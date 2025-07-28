from django.contrib import admin
from .models import Product, Purchase

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'expiry_date', 'status', 'price')
    search_fields = ('name', 'category')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity', 'total_price', 'purchase_date')
    list_filter = ('purchase_date', 'customer', 'product__category')
    search_fields = ('product__name', 'customer__username')