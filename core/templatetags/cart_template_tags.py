from django import template
from core.models import Order, Item, OrderItem

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0


@register.filter
def short_item_description(order_item):
    lines = str(order_item.item.description).split("\r", 1)
    if len(lines) > 35:
        short_description = f"{str(lines[0])[0:32]}..."
        return short_description
    else:
        return f"{str(lines[0])}..."
