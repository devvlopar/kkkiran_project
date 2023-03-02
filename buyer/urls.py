from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('faqs/', faqs, name='faqs'),
    path('privacy/', privacy, name="privacy"),
    path('term/', terms , name="ei"),
    path('add_row/', add_row, name="add_row"),
    path('register/', register, name='register'),
    path('otp/', otp, name='otp'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('cart/',cart,name='cart'),
    path('add_to_cart/<int:pk>',add_to_cart,name='add_to_cart'), 
    path('del_cart_item/<int:c_item>',del_cart_item,name='del_cart_item'), 
    path('cart/paymenthandler/', paymenthandler, name='paymenthandler'),




   
]



#html : structure
#css : styles/ looks
#JS : animation,responsiveness