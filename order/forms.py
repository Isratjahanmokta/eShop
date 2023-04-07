from django import forms
from .models import BillingAddress


class BillingForm(forms.ModelForm):
    class Meta:
        Model = BillingAddress
        fields = ['address', 'zipcode', 'city', 'country']