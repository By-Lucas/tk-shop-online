from rest_framework import routers
from django.urls import path, include

from . import views
#from products.viewsets.viwesets import ProductViewSet, CategoryViewSet

# router = routers.DefaultRouter()
# router.register('products', ProductViewSet, basename='products')
# router.register('categories', CategoryViewSet, basename='categories')

app_name='product'

urlpatterns =[
    #path('api/v1/', include(router.urls)),
    path('like-product/',  views.like_product, name='like_product'),
    path('<slug:slug>', views.ProductView.as_view(), name="product"),
    path('comment/<slug:slug>', views.post_comment, name="post_comment"),
    path('produto-favorito/<int:product_id>', views.mark_product_as_favorite, name="mark_product_as_favorite"),
    path('enviar-produto/<int:product_id>/<str:media_type>', views.SendProduct.as_view(), name="send_whatsapp_telegram"),
]
