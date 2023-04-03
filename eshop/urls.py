from django.urls import path
from .views import Home

app_name = 'eshop'

urlpatterns = [
    path('', Home.as_view(), name='home')
]
