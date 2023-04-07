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
    
class BillingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=250, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f'{self.user.profile.username} billing address'
    
    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]
        
        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True
    
    class Meta:
        verbose_name_plural = "Billing Addresses"
