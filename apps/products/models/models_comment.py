from django.db import models
from .models_product import Product
from helpers.base_models import BaseModelTimestamp


class CommentModel(BaseModelTimestamp):
    product = models.ForeignKey(Product, verbose_name="Produto", on_delete=models.CASCADE, related_name='comments')
    email = models.EmailField(verbose_name="Email")
    name = models.CharField(verbose_name="Nome", max_length=150)
    description = models.TextField(verbose_name="Comentário")

    def __str__(self):
        return self.product.name if self.product.name else self.name
    
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
