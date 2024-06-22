from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group
from .models import Product, Sale


class ProductTests(APITestCase):
    def setUp(self):
        # Crear usuarios y grupos
        self.admin_user = User.objects.create_user(username='admin', password='admin123')
        self.user = User.objects.create_user(username='user', password='user123')
        self.seller = User.objects.create_user(username='seller', password='seller123')

        admin_group = Group.objects.get(name='Administradores')
        user_group = Group.objects.get(name='Usuarios')
        seller_group = Group.objects.get(name='Vendedores')

        self.admin_user.groups.add(admin_group)
        self.user.groups.add(user_group)
        self.seller.groups.add(seller_group)

        # Crear un cliente autenticado para cada usuario
        self.admin_client = APIClient()
        self.admin_client.login(username='admin', password='admin123')

        self.user_client = APIClient()
        self.user_client.login(username='user', password='user123')

        self.seller_client = APIClient()
        self.seller_client.login(username='seller', password='seller123')

        # Crear un producto de ejemplo
        self.product = Product.objects.create(
            product_name='Laptop',
            product_type='Electronics',
            unitary_price=1000,
            product_brand='BrandA'
        )

    def test_create_product_as_admin(self):
        url = reverse('product_list')
        data = {
            'product_name': 'Smartphone',
            'product_type': 'Electronics',
            'unitary_price': 500,
            'product_brand': 'BrandB'
        }
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_as_user(self):
        url = reverse('product_list')
        data = {
            'product_name': 'Smartphone',
            'product_type': 'Electronics',
            'unitary_price': 500,
            'product_brand': 'BrandB'
        }
        response = self.user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_product_as_user(self):
        url = reverse('product-detail', args=[self.product.product_id])
        response = self.user_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product_as_admin(self):
        url = reverse('product-detail', args=[self.product.product_id])
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_as_user(self):
        url = reverse('product-detail', args=[self.product.product_id])
        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class SaleTests(APITestCase):
    def setUp(self):
        # Crear usuarios y grupos
        self.admin_user = User.objects.create_user(username='admin', password='admin123')
        self.user = User.objects.create_user(username='user', password='user123')
        self.seller = User.objects.create_user(username='seller', password='seller123')

        admin_group = Group.objects.get(name='Administradores')
        user_group = Group.objects.get(name='Usuarios')
        seller_group = Group.objects.get(name='Vendedores')

        self.admin_user.groups.add(admin_group)
        self.user.groups.add(user_group)
        self.seller.groups.add(seller_group)

        # Crear un cliente autenticado para cada usuario
        self.admin_client = APIClient()
        self.admin_client.login(username='admin', password='admin123')

        self.user_client = APIClient()
        self.user_client.login(username='user', password='user123')

        self.seller_client = APIClient()
        self.seller_client.login(username='seller', password='seller123')

        # Crear un producto y una venta de ejemplo
        self.product = Product.objects.create(
            product_name='Laptop',
            product_type='Electronics',
            unitary_price=1000,
            product_brand='BrandA'
        )

        self.sale = Sale.objects.create(
            product_id=self.product,
            quantity=2,
            unitary_price=1000
        )

    def test_create_sale_as_seller(self):
        url = reverse('sale_list')
        data = {
            'product_id': self.product.product_id,
            'quantity': 1,
            'unitary_price': 1000
        }
        response = self.seller_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_sale_as_user(self):
        url = reverse('sale_list')
        data = {
            'product_id': self.product.product_id,
            'quantity': 1,
            'unitary_price': 1000
        }
        response = self.user_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_sale_as_user(self):
        url = reverse('sale-detail', args=[self.sale.sale_id])
        response = self.user_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_sale_as_seller(self):
        url = reverse('sale-detail', args=[self.sale.sale_id])
        response = self.seller_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_sale_as_admin(self):
        url = reverse('sale-detail', args=[self.sale.sale_id])
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_sale_as_user(self):
        url = reverse('sale-detail', args=[self.sale.sale_id])
        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
