from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Product, Sale

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == 'products':
        # Crear o obtener los grupos
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        user_group, created = Group.objects.get_or_create(name='Usuarios')
        seller_group, created = Group.objects.get_or_create(name='Vendedores')

        # Definir permisos para los productos
        product_ct = ContentType.objects.get_for_model(Product)
        sale_ct = ContentType.objects.get_for_model(Sale)

        # Permisos para el grupo de administradores
        admin_permissions = [
            Permission.objects.get(codename='add_product', content_type=product_ct),
            Permission.objects.get(codename='change_product', content_type=product_ct),
            Permission.objects.get(codename='delete_product', content_type=product_ct),
            Permission.objects.get(codename='view_product', content_type=product_ct),
            Permission.objects.get(codename='add_sale', content_type=sale_ct),
            Permission.objects.get(codename='change_sale', content_type=sale_ct),
            Permission.objects.get(codename='delete_sale', content_type=sale_ct),
            Permission.objects.get(codename='view_sale', content_type=sale_ct),
        ]

        # Permisos para el grupo de usuarios (solo visualización de productos)
        user_permissions = [
            Permission.objects.get(codename='view_product', content_type=product_ct),
        ]

        # Permisos para el grupo de vendedores (agregar y ver ventas)
        seller_permissions = [
            Permission.objects.get(codename='add_sale', content_type=sale_ct),
            Permission.objects.get(codename='view_sale', content_type=sale_ct),
        ]

        # Asignar permisos a los grupos
        admin_group.permissions.set(admin_permissions)
        user_group.permissions.set(user_permissions)
        seller_group.permissions.set(seller_permissions)
