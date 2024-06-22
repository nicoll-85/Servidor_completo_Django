from django.shortcuts import render
from .models import (Product, Sale)
from .serializers import (Productserializer, Saleserializer)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import (ProductFilter, SaleFilter)
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import viewsets


# Vistas genericas Producto
class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = Productserializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = Productserializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class ProductListByBrand(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = Productserializer

    def get_queryset(self):
        product_brand = self.kwargs['product_brand']
        return Product.objects.filter(product_brand=product_brand)


class ProductListByType(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = Productserializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        product_type = self.kwargs['product_type']
        return Product.objects.filter(product_type=product_type)


# Vistas genericas Ventas
class SaleListCreate(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = Saleserializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SaleFilter
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class SaleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = Saleserializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class SaleListByDate(generics.ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = Saleserializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        date = self.kwargs['date']
        return Sale.objects.filter(date=date)


class SaleListByProduct(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = Saleserializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


# Vista propia que enlaza los modelos
class ProductSalesAPIView(APIView):
    def get(self, request, product_id):
        try:
            product_id = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        sales = Sale.objects.filter(product_id=product_id)
        sales_serializer = Saleserializer(sales, many=True)
        product_serializer = Productserializer(product_id)

        response_data = {
            'product': product_serializer.data,
            'sales': sales_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)


# Vista Viewset
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = Productserializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = Saleserializer
