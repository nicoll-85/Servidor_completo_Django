import django_filters
from .models import (Product, Sale)


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['product_brand']


class SaleFilter(django_filters.FilterSet):
    class Meta:
        model = Sale
        fields = ['sale_date']