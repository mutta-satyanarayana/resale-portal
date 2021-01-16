from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('list/', views.order_list, name='order_list'),
    path('cancel/<int:order_id>', views.order_cancel, name='cancelorder'),
]