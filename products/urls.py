from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProductListCreate, ProductDetail, ProductListByBrand, ProductListByType, SaleListCreate, SaleDetail,
                    SaleListByProduct, SaleListByDate, ProductSalesAPIView, ProductViewSet, SaleViewSet)

urlpatterns = [
    path("products/", ProductListCreate.as_view(), name="product_list"),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('products/brand/<str:brand>/', ProductListByBrand.as_view(), name='product-list-by-brand'),
    path('products/type/<str:product_type>/', ProductListByType.as_view(), name='product-list-by-type'),
    path("sales/", SaleListCreate.as_view(), name="sale_list"),
    path('sales/<int:pk>/', SaleDetail.as_view(), name='sale-detail'),
    path('sales/date/<str:date>/', SaleListByDate.as_view(), name='sale-list-by-date'),
    path('sales/product/<int:pk>/', SaleListByProduct.as_view(), name='sale-list-by-product'),
    path('product/<int:product_id>/sales/', ProductSalesAPIView.as_view(), name='product-sales')
]

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]