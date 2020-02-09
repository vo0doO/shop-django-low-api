from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from hashlib import md5
from urllib.parse import urlencode
from django import forms


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('R', 'Robokassa'),
    ('Q', 'Qiwi'),
)
 

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    country = CountryField(blank_label='(выбирете страну)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100'
        }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
