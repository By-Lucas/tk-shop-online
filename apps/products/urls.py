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
    path('<slug:slug>', views.ProductView.as_view(), name="product"),
    path('enviar-produto/<int:product_id>/<str:media_type>', views.SendProduct.as_view(), name="send_whatsapp_telegram"),
]
