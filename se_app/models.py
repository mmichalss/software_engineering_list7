from django.core.exceptions import ValidationError
from django.db import models
from unicodedata import decimal


# Create your models here.

def validate_positive(n):
    if n < 0:
        raise ValidationError('Price cannot be negative.')


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=50, decimal_places=3, validators=[validate_positive])
    available = models.BooleanField()


class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField()


class Order(models.Model):
    STATUS_CHOICES = {
        'N': 'New',
        'P': 'In Process',
        'S': 'Sent',
        'C': 'Completed'
    }
    id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)

    def price_sum(self):
        return sum(p.price for p in self.products.all())

    def validate_presence_of_products(self):
        if not all(p.available for p in self.products.all()):
            print('Some products are not available.')