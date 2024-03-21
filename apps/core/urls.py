from django.urls import path

from core.views import ProductListView, product_ofert


app_name = "home"

urlpatterns = [
    path('', ProductListView.as_view(), name="home"),
    path('oferta/', product_ofert, name="ofert"),
]
