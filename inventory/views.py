from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from datetime import timedelta
from django.utils import timezone


from .forms import ProductForm
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
            return redirect('product_list')
        else:
            message = 'Invalid username or password.'
    return render(request, 'inventory/login.html', {'message': message})


def logout_view(request):
    logout(request)
    return redirect('login')


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
    today = timezone.now().date()
    return render(request, 'inventory/product_list.html', {'products': products, 'today': today})

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

@login_required
def customer_product_list(request):
    products = Product.objects.filter(expiry_date__gte=timezone.now().date())
    return render(request, 'inventory/customer_product_list.html', {'products': products})




