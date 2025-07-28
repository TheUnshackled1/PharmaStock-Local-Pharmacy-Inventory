from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page for customers
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),


    # Admin-only product management
    path('dashboard/products/', views.product_list, name='product_list'),
    path('expired/', views.expired_products, name='expired_products'),
    path('expiring-soon/', views.expiring_soon_products, name='expiring_soon'),
    path('low-stock/', views.low_stock_products, name='low_stock'),
    path('income-report/', views.income_report, name='income_report'),
    path('add/', views.product_create, name='product_add'),
    path('edit/<int:pk>/', views.product_update, name='product_edit'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),

    # Customer shop (optional, can be removed if home.html is the shop)
    path('shop/', views.customer_product_list, name='customer_product_list'),
    path('buy/<int:pk>/', views.purchase_product, name='purchase_product'),
    path('checkout/', views.checkout, name='checkout'),
]