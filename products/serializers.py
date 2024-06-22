from rest_framework import serializers
from .models import (Product, Sale)


class Productserializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["product_id", "product_name", "product_type", "unitary_price", "product_brand"]


class Saleserializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ["sale_id", "product_id", "quantity", "unitary_price", "sale_date"]

