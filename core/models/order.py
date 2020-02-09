from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from .order_item import OrderItem
from .billing_address import BillingAddress
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        BillingAddress,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)

    payment_object_id = models.IntegerField(
        blank=True,
        null=True,
    )

    payment_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    payment = GenericForeignKey(
        'payment_content_type',
        'payment_object_id',
    )

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_qiwi_context(self):
        context = {
            "amount": self.get_total(),
            "description": "Товары",
            "user": self.user,
            "items": self.items,
            "ordered": self.ordered,
            "billing_address": self.billing_address,
            "start_date": self.start_date,
            "ordered_date": self.ordered,
            "qpk": settings.QIWI_P2P_PUBLIC_KEY,
            }
        return context