from django.db import models
from django.conf import settings
from authentication.models import CustomUser
from eshop.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.quantity} X {self.item}'
    
    def get_tot_price(self):
        total = self.item.price * self.quantity
        float_total = format(total, '.2f')
        return float_total
    
class Order(models.Model):
    order_item = models.ManyToManyField(Cart)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    
    def get_total(self):
        total = 0
        for order_items in self.order_item.all():
            total += float(order_items.get_tot_price())
        return total   
