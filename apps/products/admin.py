from django.contrib import admin

from products.models.models_product import Product
from products.models.models_comment import CommentModel


admin.site.register(Product)
admin.site.register(CommentModel)

