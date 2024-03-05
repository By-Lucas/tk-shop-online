from django.urls import path

from core.views import ProductListView, FilteredProductListView, product_ofert


app_name = "home"

urlpatterns = [
    path('', ProductListView.as_view(), name="home"),
    path('oferta/', product_ofert, name="ofert"),
    path('oferta/filtrada/', FilteredProductListView.as_view(), name='filtered_product_list'),
    
]
