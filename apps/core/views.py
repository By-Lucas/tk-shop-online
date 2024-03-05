from django.db.models import Q
from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage

from category.models import Category
from products.models.models_product import Product


class ProductListView(View):
    template_name = "core/ofert.html"
    items_per_page = 40
    
    def get(self, request):
        name = request.GET.get('name')
        store = request.GET.get('marca')
        company = request.GET.get('company')
        favorite = request.GET.get('favorite')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        selected_categories = request.GET.getlist('category')
        
        products = Product.objects.all()
        products_featured = products.filter(favorite=True)[:4]
        
        categories_with_counts = Category.objects.annotate(product_count=Count('product'))
        # Se desejar, você pode filtrar as categorias que têm produtos
        categories_with_products = categories_with_counts.filter(product_count__gt=0)
        
        if store:
            products = products.filter(company_product__name__icontains=store)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if name:
            products = products.filter(name__icontains=name)
        if favorite:
            products = products.filter(favorite=True)
        if company:
            products = products.filter(company_name__icontains=company)
        if selected_categories:
            products = products.filter(category__name__in=selected_categories)
        
        paginator = Paginator(products, self.items_per_page)
        page_number = request.GET.get('page', 1)
        try:
            products = paginator.page(page_number)
        except EmptyPage:
            products = paginator.page(1)
        
        context = {
            'products': products, 
            'products_featured': products_featured, 
            'selected_categories': selected_categories,
            'categories_with_products':categories_with_products
            }
        
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context)


class FilteredProductListView(View):
    def post(self, request):
        products = Product.objects.all()

        # Obter parâmetros de filtro da solicitação POST
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        category = request.POST.get('category')
        name = request.POST.get('name')
        favorite = request.POST.get('favorite')
        company = request.POST.get('company')

        # Aplicar filtros aos produtos
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if category:
            products = products.filter(category__name=category)
        if name:
            products = products.filter(name__icontains=name)
        if favorite:
            products = products.filter(favorite=True)
        if company:
            products = products.filter(company_name__icontains=company)
        
        

        # Serializar os produtos para JSON
        data = [{'name': product.name, 'price': product.price} for product in products]
        
        print(data)
        
        # Retornar os produtos filtrados em JSON
        return JsonResponse(data, safe=False)
    
    
def product_ofert(request):
    template_name = "products/product.html"

    return render(request,template_name)
