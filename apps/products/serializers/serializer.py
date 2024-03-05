from rest_framework import serializers

from category.models import Category
from apps.products.models.models_product import Product


class ProductSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Product
        # fields = ('id', 'company_name', 'name', 'description', 'price', 'category', 'affiliate_link',
        #           'featured', 'image', 'coupon', 'featured')
        fields = '__all__'
        
    def create(self, validated_data):
        company_name = validated_data.pop('company_name', None)
        name = validated_data.get('name')
        price = validated_data.get('price')

        # Encontre a empresa correspondente
        company_product = None
        if company_name:
            company_product, _ = ProductCompany.objects.get_or_create(name=company_name)
            validated_data['company_product'] = company_product

        # Verifique se já existe um produto com o mesmo nome e preço
        try:
            product = Product.objects.get(name=name, price=price)
            for attr, value in validated_data.items():
                setattr(product, attr, value)
            product.save()
        except Product.DoesNotExist:
            product = Product.objects.create(**validated_data)

        return product
    
    

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'image')
