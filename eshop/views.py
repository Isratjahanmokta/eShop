from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
# Create your views here.
def index(request):
    return render(request, 'base.html', context= {'title':'Home'})

class Home(ListView):
    context_object_name = 'products'
    model = Product
    queryset = Product.objects.all()
    template_name = 'eshop/home.html'
    