from django import forms
from .models import Product, Supplier, Return

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'expiry_date', 'low_stock_threshold', 'price', 'supplier', 'image']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone_number', 'address']

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['product', 'quantity', 'reason']