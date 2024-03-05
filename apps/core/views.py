from django.db.models import Q
from django.db.models import Count
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage

from category.models import Category
from apps.products.forms import ProductForm
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
        
        forms = ProductForm()
        
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
            'forms': forms,
            'products': products, 
            'products_featured': products_featured, 
            'selected_categories': selected_categories,
            'categories_with_products':categories_with_products
        }
        
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home:home')  # Redirecionar para a página de lista de produtos após a criação bem-sucedida
        else:
            # Se o formulário não for válido, renderize novamente a página com os erros do formulário
            forms = ProductForm()  # Instância de um novo formulário vazio para renderizar na página
            products = Product.objects.all()
            products_featured = products.filter(favorite=True)[:4]
            categories_with_counts = Category.objects.annotate(product_count=Count('product'))
            categories_with_products = categories_with_counts.filter(product_count__gt=0)
            context = {
                'forms': forms,
                'products': products, 
                'products_featured': products_featured, 
                'categories_with_products':categories_with_products
            }
            return render(request, self.template_name, context)


def product_ofert(request):
    template_name = "products/product.html"

    return render(request,template_name)
