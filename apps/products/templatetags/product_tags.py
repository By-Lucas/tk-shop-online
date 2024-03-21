# product_tags.py

from django import template

register = template.Library()

@register.filter
def is_favorite(product, user):
    return product.favorites.filter(user=user).exists()


@register.filter
def is_liked(product, user):
    return product.favorites.filter(user=user).exists()
