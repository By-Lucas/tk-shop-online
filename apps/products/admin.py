from django.contrib import admin

from products.models.models_comment import CommentModel
from products.models.models_product import Product, FavoriteProductLink, ProductLike


admin.site.register(Product)
admin.site.register(CommentModel)
admin.site.register(ProductLike)
admin.site.register(FavoriteProductLink)


