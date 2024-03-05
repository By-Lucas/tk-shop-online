from django.db import models
from helpers.base_models import BaseModelTimestamp


class Category(BaseModelTimestamp):
    name = models.CharField(max_length=255, verbose_name='Caterogia', null=True, blank=True)
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    image = models.ImageField(verbose_name="Imagem", null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
