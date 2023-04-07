from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('append_product/', views.append_product, name='append_product'),
    path('product/', views.product_view, name='product_list'),
    path('edit_product/<str:product_code>/',
         views.product_edit, name='edit_product'),
    path('add_product/<str:product_code>/',
         views.product_add, name='add_product'),
    path('subtract_product/<str:product_code>/',
         views.product_subtract, name='subtract_product'),
]
