from typing import Any

from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import redirect, render, get_object_or_404

from category.models import Category
from products.models.models_product import Product
from products.forms import CommentForm, ProductForm
from config.models.models_config import ConfigModel
from products.models.models_comment import CommentModel
from config.models.models_telegram import TelegramGroups
from config.models.models_whatsapp import WhtasappGroups
from helpers.apis.whatsapp_api import send_to_whatsapp_group
from helpers.apis.telegram_api import send_media_with_description
from helpers.utils import domain_company, get_formatted_description

from django.contrib.sites.shortcuts import get_current_site


# Create your views here.
class ProductView(View):
    template_name = "products/product-view.html"

    def get(self, request, slug, *args: Any, **kwargs: Any):
        oferts_page = True
        user = self.request.user

        product = get_object_or_404(Product, slug_product=slug)
        comments = CommentModel.objects.filter(product=product).order_by("-created_date")[:5]
        form = ProductForm(instance=product)
        
        #featured_products = Product.objects.all()
        featured_products = Product.objects.all().exclude(id=product.id)[:10]  # Obtém até 20 produtos
        #product_chunks = list(chunk_it(featured_products, 4)) # Aqui mostra de 4 em 4 produtos

        context = {
            'form': form,
            'product': product,
            'comments': comments,
            'oferts_page':oferts_page,
            'category': Category.objects.all(),
            'product_chunks': featured_products,
        }
        return render(request, self.template_name, context)
    
    def get_object(self, queryset=None):
        return Product.objects.filter(pk=self.kwargs.get("pk"))

    def post(self, request, slug, *args: Any, **kwargs: Any):
        x_frame_options = request.META.get("X-Frame-Options")
        if x_frame_options is not None:
            print("X-Frame-Options:", x_frame_options)
        
        product = get_object_or_404(Product, slug_product=slug)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product:product', slug=product.slug_product)  # Corrigido aqui
        
        return redirect('product:product', slug=product.slug_product)  # Corrigido aqui

            
class SendProduct(View):
    def post(self, request,  *args: Any, **kwargs: Any):
        if request.method == "POST":
            send_telegram = None
            send_whatsapp = None
            product_id:int = self.request.POST.get("product_id", None)
            media_type:str = self.request.POST.get("media_type", None)
            
            config = ConfigModel.objects.all().first()
            product = get_object_or_404(Product, pk=product_id)
            if not product:
                return JsonResponse({'success': False, 'message': 'Produto não existe'})
            
            chat_ids_telegram = TelegramGroups.objects.filter(send_msg=True).values_list('group_id', flat=True)
            chat_ids_whatsapp = WhtasappGroups.objects.filter(send_msg=True).values_list('group_id', flat=True)
            
            message = get_formatted_description(config.send_product_description, config.offer_group, instance=product)
            
            if media_type.lower() == "whatsapp":
                if config.send_product_group:
                    try:
                        if product.image:
                            send_whatsapp = send_to_whatsapp_group(caption=message,
                                                                media_link=f'{get_current_site(request)}{product.image.url}',
                                                                list_chat_id=chat_ids_whatsapp,
                                                                )
                            
                            if 'error' in send_whatsapp:
                                return JsonResponse({'success': False, 'message': f'Opção para envio de mensagens para {media_type.upper()}|[ERROR]: {send_whatsapp["error"]} .'})
                            
                            if send_whatsapp:
                                return JsonResponse({'success': True, 'message':"Produto enviado para os grupos Whatsapp"})
                            
                    except Exception as e:
                        return JsonResponse({'success': False, 'message': str(e)})
                else:
                    return JsonResponse({'success': False, 'message': f'Opção para envio de mensagens para {media_type.upper()} está desabilitado.'})
                        
            if media_type.lower() == "telegram":
                if config.send_product_group:
                    try:
                        if product.image:
                            send_telegram = send_media_with_description(media_path=product.image.path, 
                                                                    chat_id=chat_ids_telegram, 
                                                                    description=message, 
                                                                    parse_mode="Markdown", 
                                                                    notify=True)
                            if send_telegram:
                                return JsonResponse({'success': True, 'message':"Produto enviado para os grupos Telegram"})
                    except Exception as e:
                        return JsonResponse({'success': False, 'message': str(e)})
                else:
                    return JsonResponse({'success': False, 'message': f'Opção para envio de mensagens para {media_type.upper()} está desabilitado.'})
                    
        return JsonResponse({'success': False, 'message': 'Requisição inválida'})


def post_comment(request, slug):
    product = get_object_or_404(Product, slug_product=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            messages.success(request, 'Seu comentário foi enviado com sucesso!')
            return redirect('product:product', slug=product.slug_product)
        else:
            messages.error(request, 'Houve um erro ao enviar seu comentário. Por favor, tente novamente.')
    
    return redirect('product:product', slug=slug)
    
