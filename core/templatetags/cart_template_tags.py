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
def short_item_description(slug):
    item = Item.objects.get(slug=slug)
    if len(item.description) > 100:
        short_description = f"{item.description[0:97]}..."
        return short_description
    return item.description
