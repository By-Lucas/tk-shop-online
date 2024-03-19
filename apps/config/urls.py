from django.urls import path

from . import views


app_name='config'

urlpatterns =[
    path('grupos-whatsapp/', views.get_groups_whatsapp, name='grupos_whatsapp'),
    path('my-grupos-whatsapp/', views.get_my_groups_whatsapp, name='get_my_groups_whatsapp'),
    path('salvar-groupo-whatsapp/', views.save_selected_groups, name='save_selected_groups'),
    path('deletar-groupo-whatsapp/<int:pk>', views.delete_group, name='delete_group'),
]
