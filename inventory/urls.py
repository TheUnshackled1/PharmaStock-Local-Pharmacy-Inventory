from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('expired/', views.expired_products, name='expired_products'),
    path('expiring-soon/', views.expiring_soon_products, name='expiring_soon'),
    path('add/', views.product_create, name='product_add'),
    path('edit/<int:pk>/', views.product_update, name='product_edit'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
]