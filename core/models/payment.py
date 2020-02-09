from django.conf import settings
from django.db import models
from pprint import pprint
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from robokassa.signals import result_received
from django.contrib.contenttypes.fields import GenericRelation


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    order_items = GenericRelation(
        'Order',
        'payment_object_id',
        'payment_content_type_id',
        related_query_name='payments',
    )


class Stripe(Payment):
    stripe_charge_id = models.CharField(max_length=50)


class Robo(Payment):
    InvId = models.IntegerField(u'Номер заказа', db_index=True)

    class Meta:
        verbose_name = u'Уведомление об успешном платеже'
        verbose_name_plural = u'Уведомления об успешных платежах (ROBOKASSA)'
        
    def __unicode__(self):
        return u'#%d' % (self.InvId)


class Qiwi(Payment):
    invoice_uid = models.UUIDField()
