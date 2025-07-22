from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()

    def is_expired(self):
        return timezone.now().date() > self.expiry_date

    def days_until_expiry(self):
        return (self.expiry_date - timezone.now().date()).days

    @property
    def status(self):
        if self.is_expired:
            return "Expired"
        elif self.days_until_expiry <= 7:
            return "Expiring Soon"
        return "Fresh"

    def __str__(self):
        return f"{self.name} ({self.status})"