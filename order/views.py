from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from order.models import Cart, Order
from eshop.models import Product
from django.contrib import messages

# Create your views here.

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_items = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_item.filter(item=item).exists():
            order_items[0].quantity += 1
            order_items[0].save()
            messages.info(request, "This item quantity was updated.")
            return redirect("eshop:home")
        else:
            order.order_item.add(order_items[0])
            messages.info(request, "This item was added to your cart.")
            return redirect("eshop:home")
    else:
        order = Order(user=request.user)
        order.save()
        order.order_item.add(order_items[0])
        messages.info(request, "This item was added to your cart.")
        return redirect("eshop:home")
 
@login_required           
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render (request, 'order/cart.html', context = {'carts':carts, 'order':order})
    else:
        messages.warning(request, 'You do not have any item in your cart!')
        return redirect('eshop:home')