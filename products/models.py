from django.db import models
from datetime import date
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, )
    product_type = models.CharField(max_length=150)
    unitary_price = models.IntegerField()
    product_brand = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.product_id


class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unitary_price = models.IntegerField()
    sale_date = models.DateField(default=date.today)

    def __str__(self) -> str:
        return self.sale_id



