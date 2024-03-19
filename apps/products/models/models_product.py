import os
import uuid
import random

from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save

from category.models import Category
from stores.models import ProductStore
from helpers.base_models import BaseModelTimestamp
from config.models.models_config import ConfigModel
from config.models.models_telegram import TelegramGroups
from config.models.models_whatsapp import WhtasappGroups
from helpers.apis.whatsapp_api import send_to_whatsapp_group
from helpers.apis.telegram_api import send_media_with_description
from helpers.utils import delete_products, get_formatted_description


def image_company(instance, filename):
    unique_filename = f"company/{instance.name}/{uuid.uuid4()}-{filename}"
    return unique_filename

def product_image_path(instance, filename):
    # Gere um UUID único para cada imagem
    unique_filename = f"product_{uuid.uuid4()}{filename}"
    return unique_filename

def generate_unique_number():
    # Gera um número único de até 5 dígitos
    return random.randint(10000, 99999)

class Product(BaseModelTimestamp):
    name = models.CharField(max_length=255, verbose_name='Produto', null=True, blank=True)
    company_name = models.CharField(max_length=255, verbose_name='Nome da empresa que o produto faz parte',help_text="Exemplo: Amazon, Aliexpress", null=True, blank=True)
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço', null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name="Categoria", on_delete=models.DO_NOTHING, null=True, blank=True)
    affiliate_link = models.CharField(max_length=2000, verbose_name='Link de afilidado', null=True, blank=True)
    coupon = models.CharField(max_length=200, verbose_name='Cupom', null=True, blank=True)
    favorite  = models.BooleanField(verbose_name="Favorito", null=True, blank=True, default=False)
    image = models.FileField(verbose_name="Imagem", null=True, max_length=250, blank=True, help_text="A dimensão da imagem deve ser 160x160", upload_to=product_image_path)
    is_video = models.BooleanField(verbose_name="É vídeo?", null=True, blank=True, default=False)
    resend_product = models.BooleanField(verbose_name="Reenviar produto para os grupos?", null=True, blank=True, default=False)
    company_product = models.ForeignKey(ProductStore, verbose_name="Shop online do produto", on_delete=models.DO_NOTHING, null=True, blank=True)
    product_description = models.TextField(verbose_name='Descrição para envio da mensagem', null=True, blank=True, 
                                               default="""✅{titulo}✅\n
                                               🔥 R${preco}
                                               🔖 Use o cupom: {cupom}
                                               🛍 Compre aqui: {link_produto}
                                               \n😄 Convide seus amigos e familiares para participarem dos nossos grupos de promoção: {link_do_grupo}
                                               \n⚠ O link da foto na promo, Não está Clicável? É só adicionar um dos ADMS em seus contatos""".encode("utf-8"),
                                               help_text="Alem das informações princioais, digite aqui outra informação que deseja enviar: Use o modelo descrito como base")
    
    slug_product = models.SlugField(unique=True, max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else str(self.id)
    
    def save(self, *args, **kwargs):
        config = ConfigModel.objects.all().first()        
        
        if self.image and os.path.splitext(self.image.name)[1] == '.mp4':
            self.is_video = True
        else:
            self.is_video = False
            
        if not self.slug_product:
            base_slug = slugify(self.name)  # Gera o slug a partir do título do produto
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug_product=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug_product = slug
        
        delete_products(Product.objects.all(), config.time_hours_product)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product:product', kwargs={'slug': self.slug_product})  # ou slug=self.slug, se estiver usando slug
            
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


#@receiver(post_save, sender=Product)
def post_save_create_product_receiver(sender, instance, created, **kwargs):
    config = ConfigModel.objects.all().first()
    chat_ids = TelegramGroups.objects.filter(send_msg=True).values_list('group_id', flat=True)
    chat_ids_whatsapp = WhtasappGroups.objects.filter(send_msg=True).values_list('group_id', flat=True)
    
    description = ""
    
    if created:
        if config.send_product_group and instance.resend_product:
            if instance:
                if not instance.product_description:
                    description = get_formatted_description(config.send_product_description, config.offer_group, instance)
                else:
                    description = get_formatted_description(instance.product_description, config.offer_group, instance)
                    
                send_telegram = send_media_with_description(#media_path=instance.image.path, 
                                                            chat_id=chat_ids, 
                                                            description=description, 
                                                            parse_mode="Markdown", 
                                                            notify=True)
                    
                send_whatsapp = send_to_whatsapp_group(list_chat_ids=chat_ids_whatsapp,
                                                        #media_link=instance.image.path,
                                                        caption=description)
                    
            else:
                print('Produto não contem imagem')
            
            if instance.resend_product:
                instance.resend_product = False
                instance.save()
                print('PRODUCO CRIADO E ENVIADO AO TELEGRAM')
            
        
#@receiver(pre_save, sender=Product)
def pre_save_product_receiver(sender, instance, **kwargs):
    config = ConfigModel.objects.all().first()
    chat_ids = TelegramGroups.objects.filter(send_msg=True).values_list('group_id', flat=True)
    chat_ids_whatsapp = WhtasappGroups.objects.filter(send_msg=True).values_list('group_id', flat=True)
    
    description = ""
    if instance.pk:
        if config.send_product_group and instance.resend_product:
            if instance:
                if not instance.product_description:
                    description = get_formatted_description(config.send_product_description, config.offer_group, instance)
                else:
                    description = get_formatted_description(instance.product_description, config.offer_group, instance)
                    
                send_telegram = send_media_with_description(#media_path=instance.image.path, 
                                                            chat_id=chat_ids, 
                                                            description=description, 
                                                            parse_mode="Markdown", 
                                                            notify=True)
                
                send_whatsapp = send_to_whatsapp_group(list_chat_ids=chat_ids_whatsapp,
                                                        #media_link=instance.image.path,
                                                        caption=description)
       
            else:
                print('Produto não contem imagem')

            if instance.resend_product:
                instance.resend_product = False
                instance.save()
                print('PRODUTO EDITADO REENVIADO PARA OS GRUPOS')

