from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    low_stock_threshold = models.PositiveIntegerField(default=10)

    def is_expired(self):
        return timezone.now().date() > self.expiry_date

    def days_until_expiry(self):
        return (self.expiry_date - timezone.now().date()).days

    @property
    def is_low_stock(self):
        return self.quantity < self.low_stock_threshold

    @property
    def status(self):
        if self.is_expired():
            return "Expired"
        elif self.days_until_expiry() <= 7:
            return "Expiring Soon"
        elif self.is_low_stock:
            return "Low Stock"
        return "Fresh"

    def __str__(self):
        return f"{self.name} ({self.status})"

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase of {self.quantity} x {self.product.name} by {self.customer.username} on {self.purchase_date.strftime('%Y-%m-%d %H:%M')}"