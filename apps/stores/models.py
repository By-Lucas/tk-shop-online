from typing import Iterable
from django.db import models
from django.utils.text import slugify

from helpers.utils import image_company_path
from helpers.base_models import BaseModelTimestamp


class ProductStore(BaseModelTimestamp):
    name = models.CharField(max_length=200, verbose_name='Nome da empresa', null=True, blank=True, help_text="Exemplo: Aliexpress, Shopee, Amazon, Mercado Livre...")
    image = models.ImageField(verbose_name="Imagem da empresa", upload_to=image_company_path, null=True, blank=True, help_text="A dimensão da imagem deve ser 160x160")
    slug = models.SlugField(verbose_name="Nome a exibir na URL (Slug)",null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.name if self.name else (self.id)
    
    def save(self, *args, **kwargs) -> None:
        
        if not self.slug:
            base_slug = slugify(self.name)  # Gera o slug a partir do título do produto
            slug = base_slug
            counter = 1
            while ProductStore.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
            
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Loja do produto"
        verbose_name_plural = "Lojas dos produtos"
        
