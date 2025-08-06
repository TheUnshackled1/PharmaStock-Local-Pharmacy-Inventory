from django import forms
from .models import Product, Supplier, Return

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'price', 'low_stock_threshold', 'expiry_date', 'supplier']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone_number', 'address']

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['product', 'quantity', 'reason']