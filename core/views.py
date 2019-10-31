from django.utils import timezone
from .forms import CheckoutForm
from django.contrib import messages
from .models import Item, OrderItem, Order, BillingAddress, Payment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(View):
    def get(self, *args, **kwargs):
        # form
        form = CheckoutForm()
        context = {
            "form": form
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: добавить функциональность в эти поля
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                if payment_option == "S":
                    return redirect('core:stripe-payment', payment_option='stripe')
                elif payment_option == "P":
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(self.request, "Ошибка оформления")
                    return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "У Вас нет активных заказов")
            return redirect("core:order-summary")


class StripePaymentView(View):
    def get(self, *args, **kwarg):
        # order
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, 'payment.html', context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token)

            # создаем объект платежа
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # назначить эту оплату этому заказу

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Ваш заказ оформлен успешно!")
            return redirect("/")

        except stripe.error.CardError as e:
            # Так как это снижение, stripe.error.CardError будет пойман
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Ошибка ограничения пропускной способности")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Неверные параметры")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Не проверки подлинности")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Ошибка сети")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Что-то пошло не так. Вы где не обвинение. Пожалуйста, попробуйте еще раз.")
            return redirect("/")

        except Exception as e:
            # Send an email to ourselves
            messages.error(self.request, "Произошла серьезная ошибка. Вам отправленно e-mail уведомление.")
            return redirect("/")


class ProductDetailView(DetailView):
    model = Item
    template_name = "product.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "У Вас нет активных заказов")
            return redirect("/")


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


@login_required
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
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, f"{item.title} добавлен в корзину")
            return redirect("core:order-summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, f"{item.title} добавлен в корзину")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        # проверяем если ордерный предмет в ордере
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
                )[0]
            order.items.remove(order_item)
            messages.info(request, f"{item.title} удален из Вашей корзины")
            return redirect("core:order-summary")
        else:
            messages.info(request, f"В вашем заказе нет {item.title}")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, f"В вашем заказе нет {item.title}")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        # проверяем если ордерный предмет в ордере
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
                )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, f"Кол- во товара в корзине обновлено")
            return redirect("core:order-summary")
        else:
            messages.info(request, f"В вашем заказе нет {item.title}")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, f"В вашем заказе нет {item.title}")
        return redirect("core:product", slug=slug)
