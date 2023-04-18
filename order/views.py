from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from order.models import Cart, Order, BillingAddress
from eshop.models import Product
from order.forms import BillingForm
from django.contrib import messages

#for payment
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket

# Create your views here.


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_items = Cart.objects.get_or_create(
        item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_item.filter(item=item).exists():
            order_items[0].quantity += 1
            order_items[0].save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order:cart")
        else:
            order.order_item.add(order_items[0])
            messages.info(request, "This item was added to your cart.")
            return redirect("order:cart")
    else:
        order = Order(user=request.user)
        order.save()
        order.order_item.add(order_items[0])
        messages.info(request, "This item was added to your cart.")
        return redirect("order:home")


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'order/cart.html', context={'carts': carts, 'order': order})
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
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False)[0]
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
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(
                    request, f'{item.name} has been added in your cart')
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
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(
                    request, f'{item.name} has been removed from your cart')
                return redirect("order:cart")
            else:
                order.order_item.remove(order_item)
                order_item.delete()
                messages.info(
                    request, f'{item.name} has been removed from your cart')
                return redirect("order:cart")
        else:
            messages.info(request, f'{item.name} is not in your cart')
            return redirect("eshop:home")
    else:
        messages.info(request, "You don't have any active order")
        return redirect("eshop:home")


@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)

            messages.success(request, f" Shipping Address Saved!")
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    cart_qs = Cart.objects.filter(user=request.user, purchased=False)
    order_item = order_qs[0].order_item.all()
    order_total = order_qs[0].get_total()
    return render(request, 'order/checkout.html', context={'form': form, 'order_items': order_item, 'order_total': order_total, 'cart_items':cart_qs, 'saved_address':saved_address})

@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.info(request, f"Please complete shipping address")
        return redirect("order:checkout")
    
    if not request.user.profile.is_fully_filled():
        messages.info(request, f"Please complete profile details")
        return redirect("authentication:edit_profile")
    
    store_id = 'abc643507093245d'
    api_key = 'abc643507093245d@ssl' 
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=api_key)
    
    status_url = request.build_absolute_uri(reverse("order:complete"))
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_item.all()
    item_counts = order_qs[0].order_item.count()
    order_total = order_qs[0].get_total()
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed', product_name=order_items, num_of_item=item_counts, shipping_method='Courier', product_profile='None')
    
    current_user = request.user
    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user, address1=current_user.profile.address, address2=current_user.profile.address, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=saved_address, city=saved_address.city, postcode=saved_address.zipcode, country=saved_address.country)
    
    response_data = mypayment.init_payment()
    print(response_data)
    return redirect(response_data['GatewayPageURL'])

def payment_complete(request):
    return render(request, "order/payment.html")
        
