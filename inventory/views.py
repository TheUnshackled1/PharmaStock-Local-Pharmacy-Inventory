from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from datetime import timedelta
from django.utils import timezone

from .forms import ProductForm



def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form, 'action': 'Add'})

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


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    today = timezone.now().date()
    return render(request, 'inventory/product_list.html', {'products': products, 'today': today})

def expired_products(request):
    today = timezone.now().date()
    products = Product.objects.filter(expiry_date__lt=today)
    return render(request, 'inventory/expired_products.html', {'products': products})

def expiring_soon_products(request):
    today = timezone.now().date()
    soon = today + timedelta(days=7)
    products = Product.objects.filter(expiry_date__range=[today, soon])
    return render(request, 'inventory/expiring_soon.html', {'products': products})

