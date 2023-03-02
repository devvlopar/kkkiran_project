from .views import *
from django.urls import path

urlpatterns = [ 
    path('', seller_index, name='seller_index'),
    path('seller_register/', seller_register, name='seller_register'),
    path('seller_login/', seller_login, name='seller_login'),
    path('seller_logout/', seller_logout, name='seller_logout'),
    path('seller_edit_profile/', seller_edit_profile, name='seller_edit_profile'),
    path('add_product/', add_product, name='add_product'),
    # path(CHROME browser ma URL bar, views ma function nu naam, name= html pages par {% url 'url_name' %})
    path('my_product/', mere_products, name='my_product'),
    path('product_edit/<int:pk>', product_edit, name='product_edit'),
    path('product_delete/<int:pk>', product_delete, name='product_delete'),







]