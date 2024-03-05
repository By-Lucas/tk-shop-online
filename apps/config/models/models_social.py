from django.db import models

from helpers.utils import image_company_path
from helpers.base_models import BaseModelTimestamp


class SocialMedia(BaseModelTimestamp):
    name = models.CharField(verbose_name="Nome da rede social", max_length=2000, null=True, blank=True)
    image = models.FileField(verbose_name="Imagem", null=True, blank=True, upload_to=image_company_path, help_text="Imagem exibição das redes sociais.")
    url_image = models.ImageField(max_length=2000, verbose_name='URL da imagem/video', null=True, blank=True, help_text="Caso nao queira fazer upload de da imagem, cole a URL da imagem aqui")
    url_social = models.URLField(max_length=2000, verbose_name='URL da rede social', null=True, blank=True)
    
    def __str__(self):
        return self.name if self.name else (self.id)
    
    class Meta:
        verbose_name = "Redes sociais"
        verbose_name_plural = "Redes sociais"
