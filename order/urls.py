from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('add/<pk>', views.add_to_cart, name='add_to_cart'),
    path('cart_view/', views.cart_view, name='cart'),
    path('remove/<pk>/', views.remove_item, name='remove'),
    path('increase/<pk>/', views.increase_item, name='increase'),
    path('decrease/<pk>/', views.decrease_item, name='decrease'),
    path('checkout/', views.checkout, name='checkout'),
    path('pay/', views.payment, name='payment'),
    path('status/', views.payment_complete, name='complete'),
    path('purchase/<val_id>/<tran_id>/', views.purchase, name='purchase'),
    path('my_order/', views.my_order, name='order')
]
