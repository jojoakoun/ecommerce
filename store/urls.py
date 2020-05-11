from django.urls import path
from . import views

urlpatterns = [
    #This is the path for the main page:store.html 
    path('',views.store, name='store'),
    #This is the path for the cart.html page 
    path('cart/',views.cart, name='cart'),
    #This is the path for the checkout.html page 
    path('checkout/',views.checkout, name='checkout'),
    #This is the path for updating item in a view
    path('update_item/', views.updateItem, name='update_item'),
    #This is the path for the process Order view
    path('process_order/',views.processOrder, name='process_order'),
]
