from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework import permissions, authentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from category.models import Category
from apps.products.models.models_product import Product
from products.serializers.serializer import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()
        else:
            raise PermissionDenied('Você não tem permissão para acessar este recurso.')

    def get_error_message(self):
        return 'Você não tem permissão para acessar este recurso.'
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]

    def get_queryset(self):
        if self.request.user.is_superuser:
            query = Category.objects.all()
            return query
        else:
            raise PermissionDenied('Você não tem permissão para acessar este recurso.')
    
    def get_error_message(self):
        return 'Você não tem permissão para acessar este recurso.'
