from django.utils import timezone
from django.contrib import messages
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect


def checkout(request):
    return render(request, "checkout.html")


class ProductDetailView(DetailView):
    model = Item
    template_name = "product.html"


class HomeView(ListView):
    model = Item
    template_name = "home.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # проверяем если ордерный предмет в ордере
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"Кол- во {item.title} в корзине обновлено")
        else:
            order.items.add(order_item)
            messages.info(request, f"{item.title} добавлен в корзину")
            
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, f"{item.title} добавлен в корзину")
    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # проверяем если ордерный предмет в ордере
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, f"{item.title} удален из Вашей корзины")
        else:
            messages.info(request, f"В вашем заказе нет {item.title}")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, f"В вашем заказе нет {item.title}")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)
