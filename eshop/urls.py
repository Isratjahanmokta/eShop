from django.urls import path
from .views import Home, ProductDetails

app_name = 'eshop'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('product/<pk>/', ProductDetails.as_view(), name='product_details'),
]
