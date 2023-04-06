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
    
@login_required
def remove_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_item.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.order_item.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was romoved from your cart!")
            return redirect("order:cart")
    else:
        messages.info(request, "You don't have an activate order!")
        return redirect("eshop:home")
    
@login_required
def increase_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_item.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f'{item.name} has been added in your cart')
                return redirect("order:cart")
        else:
            messages.info(request, f'{item.name} is not in your cart')
            return redirect("eshop:home")
    else:
        messages.info(request, "You don't have any active order")
        return redirect("eshop:home")
    
@login_required
def decrease_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_item.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f'{item.name} has been removed from your cart')
                return redirect("order:cart")
            else:
                order.order_item.remove(order_item)
                order_item.delete()
                messages.info(request, f'{item.name} has been removed from your cart')
                return redirect("order:cart")
        else:
            messages.info(request, f'{item.name} is not in your cart')
            return redirect("eshop:home")
    else:
        messages.info(request, "You don't have any active order")
        return redirect("eshop:home")
    
    