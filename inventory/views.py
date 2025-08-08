from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Purchase, Supplier, Return
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
import pandas as pd
from django.contrib.auth.models import User
from django.http import HttpResponse
import barcode
from barcode.writer import ImageWriter

from datetime import date

from .forms import ProductForm, SupplierForm, ReturnForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


LOGIN_URL = 'login'

def home(request):
    products = Product.objects.filter(quantity__gt=0, expiry_date__gte=timezone.now().date())
    return render(request, 'inventory/home.html', {'products': products})


def login_view(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('customer_product_list')
        else:
            message = 'Invalid username or password.'
    return render(request, 'inventory/login.html', {'message': message})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('customer_product_list')
    else:
        form = SignUpForm()
    return render(request, 'inventory/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_staff)(view_func))
    return decorated_view_func

@admin_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form, 'action': 'Add'})

@admin_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form, 'action': 'Edit'})


@admin_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})


@admin_required
def product_list(request):
    products = Product.objects.all()
    low_stock_count = sum(1 for p in products if p.is_low_stock)
    today = timezone.now().date()
    return render(request, 'inventory/product_list.html', {'products': products, 'today': today, 'low_stock_count': low_stock_count})

@admin_required
def expired_products(request):
    today = timezone.now().date()
    products = Product.objects.filter(expiry_date__lt=today)
    return render(request, 'inventory/expired_products.html', {'products': products})

@admin_required
def expiring_soon_products(request):
    today = timezone.now().date()
    soon = today + timedelta(days=7)
    products = Product.objects.filter(expiry_date__range=[today, soon])
    return render(request, 'inventory/expiring_soon.html', {'products': products})

@admin_required
def low_stock_products(request):
    products = [p for p in Product.objects.all() if p.is_low_stock]
    return render(request, 'inventory/low_stock_products.html', {'products': products})

@admin_required
def income_report(request):
    purchases = Purchase.objects.all()
    total_income = sum(purchase.total_price for purchase in purchases)
    
    # You can add more complex filtering/aggregation here if needed
    # For example, income by month, by product, etc.

    context = {
        'purchases': purchases,
        'total_income': total_income,
    }
    return render(request, 'inventory/income_report.html', context)

@login_required
def customer_product_list(request):
    products = Product.objects.all()  # or filter as you prefer
    today = date.today()
    return render(request, 'inventory/customer_product_list.html', {
        'products': products,
        'today': today
    })

@login_required
def purchase_product(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        try:
            quantity_to_buy = int(request.POST.get('quantity', 1))
        except ValueError:
            messages.error(request, "Invalid quantity.")
            return redirect('customer_product_list')

        if quantity_to_buy <= 0:
            messages.error(request, "Quantity must be at least 1.")
            return redirect('customer_product_list')

        if product.quantity >= quantity_to_buy:
            # Don't decrease stock here yet, do it in checkout
            # product.quantity -= quantity_to_buy
            # product.save()
            total_cost = product.price * quantity_to_buy
            request.session['purchase_info'] = {
                'product_id': product.pk,
                'quantity': quantity_to_buy,
                'total_cost': str(total_cost) # Store as string to avoid Decimal serialization issues
            }
            return redirect('checkout')
        else:
            messages.error(request, f"Not enough {product.name} in stock. Available: {product.quantity}.")
    return redirect('customer_product_list')

@login_required
def checkout(request):
    purchase_info = request.session.get('purchase_info')
    if not purchase_info:
        messages.error(request, "No purchase information found. Please select a product first.")
        return redirect('customer_product_list')

    product = get_object_or_404(Product, pk=purchase_info['product_id'])
    quantity = purchase_info['quantity']
    total_cost = float(purchase_info['total_cost'])

    if request.method == 'POST':
        try:
            payment_amount = float(request.POST.get('payment_amount'))
        except (ValueError, TypeError):
            messages.error(request, "Invalid payment amount.")
            return render(request, 'inventory/checkout.html', {
                'product': product,
                'quantity': quantity,
                'total_cost': total_cost,
                'change': None
            })

        if payment_amount < total_cost:
            messages.error(request, "Payment amount is less than the total cost.")
            return render(request, 'inventory/checkout.html', {
                'product': product,
                'quantity': quantity,
                'total_cost': total_cost,
                'change': None
            })
        else:
            change = payment_amount - total_cost
            # Deduct stock here
            if product.quantity >= quantity:
                product.quantity -= quantity
                product.save()

                # Create a Purchase record
                from .models import Purchase # Import here to avoid circular dependency if Product is not yet defined
                Purchase.objects.create(
                    product=product,
                    customer=request.user,
                    quantity=quantity,
                    total_price=total_cost
                )

                messages.success(request, f"Purchase successful! Your change is ₱{change:.2f}.")
                del request.session['purchase_info'] # Clear session data
                return redirect('customer_product_list')
            else:
                messages.error(request, f"Not enough {product.name} in stock. Available: {product.quantity}.")
                del request.session['purchase_info'] # Clear session data
                return redirect('customer_product_list')

    return render(request, 'inventory/checkout.html', {
        'product': product,
        'quantity': quantity,
        'total_cost': total_cost,
        'change': None
    })

@admin_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})

@admin_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'inventory/supplier_form.html', {'form': form, 'action': 'Add'})

@admin_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'inventory/supplier_form.html', {'form': form, 'action': 'Edit'})

@admin_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'inventory/supplier_confirm_delete.html', {'supplier': supplier})

@admin_required
def sales_forecast(request):
    purchases = Purchase.objects.all().values('product__name', 'purchase_date', 'quantity')
    if not purchases:
        return render(request, 'inventory/sales_forecast.html', {'forecast': {}})

    df = pd.DataFrame(list(purchases))
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    df = df.set_index('purchase_date')

    forecast = {}
    for product_name, group in df.groupby('product__name'):
        daily_sales = group['quantity'].resample('D').sum()
        moving_average = daily_sales.rolling(window=7).mean().iloc[-1]
        forecast[product_name] = moving_average if not pd.isna(moving_average) else 0

    return render(request, 'inventory/sales_forecast.html', {'forecast': forecast})

@login_required
def request_return(request):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            return_request = form.save(commit=False)
            return_request.customer = request.user
            return_request.save()
            messages.success(request, "Return request submitted successfully.")
            return redirect('customer_product_list')
    else:
        form = ReturnForm()
    return render(request, 'inventory/request_return.html', {'form': form})

@admin_required
def manage_returns(request):
    returns = Return.objects.all()
    return render(request, 'inventory/manage_returns.html', {'returns': returns})

@admin_required
def process_return(request, pk, status):
    return_request = get_object_or_404(Return, pk=pk)
    if status in ["Approved", "Rejected"]:
        return_request.status = status
        if status == "Approved":
            product = return_request.product
            product.quantity += return_request.quantity
            product.save()
        return_request.save()
        messages.success(request, f"Return request {status.lower()}.")
    else:
        messages.error(request, "Invalid status.")
    return redirect('manage_returns')

def view_barcode(request, pk):
    product = get_object_or_404(Product, pk=pk)
    EAN = barcode.get_barcode_class('ean13')
    ean = EAN(f'{product.pk:012d}', writer=ImageWriter())
    response = HttpResponse(content_type='image/png')
    ean.write(response)
    return response