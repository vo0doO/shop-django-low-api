from django.contrib import admin
from .models import *
from robokassa.models import *

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


# @admin.register(SuccessNotification)
# class SuccessNotificationAdmin(admin.ModelAdmin):
    # list_display = ['InvId', 'OutSum', 'created_at']


admin.site.register(Item)
admin.site.register(OrderItem)
# admin.site.register(Order)
admin.site.register(Stripe)
admin.site.register(Robo)
