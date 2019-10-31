from django.urls import path
from .views import (
    HomeView,
    ProductDetailView,
    OrderSummaryView,
    CheckoutView,
    StripePaymentView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,)


app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
    path('product/<slug>/', ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name="remove-single-item-from-cart"),
    path('payment/<payment_option>/', StripePaymentView.as_view(), name="stripe-payment"),
]
