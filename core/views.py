# TODO: https://www.avito.ru/vyborg/avtomobili/geely_fc_vision_2008_1845368483

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.utils import timezone
from django.views.generic import DetailView, ListView, View
# from robokassa.forms import RobokassaForm
from typing_extensions import Protocol

from .forms import CheckoutForm
from .models import BillingAddress, Item, Order, OrderItem, Robo, Stripe, Qiwi


class CheckoutView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        # form
        form = CheckoutForm()
        context = {
            "form": form,
            "order": order
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == "S":
                    street_address = form.cleaned_data.get('street_address')
                    apartment_address = form.cleaned_data.get('apartment_address')
                    country = form.cleaned_data.get('country')
                    zip = form.cleaned_data.get('zip')
                    # TODO: добавить функциональность в эти поля
                    # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                    # save_info = form.cleaned_data.get('save_info')
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
                    return redirect('core:payment-stripe')

                elif payment_option == "R":
                    street_address = form.cleaned_data.get('street_address')
                    apartment_address = form.cleaned_data.get('apartment_address')
                    country = form.cleaned_data.get('country')
                    zip = form.cleaned_data.get('zip')
                    # TODO: добавить функциональность в эти поля
                    # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                    # save_info = form.cleaned_data.get('save_info')
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
                    return redirect('robokassa:buy')

                elif payment_option == "Q":
                    street_address = form.cleaned_data.get('street_address')
                    apartment_address = form.cleaned_data.get('apartment_address')
                    country = form.cleaned_data.get('country')
                    zip = form.cleaned_data.get('zip')
                    # TODO: добавить функциональность в эти поля
                    # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                    # save_info = form.cleaned_data.get('save_info')
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

                    return redirect('core:payment-qiwi')

            else:
                messages.warning(self.request, "Ошибка оформления")
                return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "У Вас нет активных заказов")
            return redirect("core:order-summary")


class StripePaymentView(View):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    def get(self, *args, **kwarg):
        # order
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order,
            'STRIPE_SECRET_KEY': settings.STRIPE_SECRET_KEY
        }
        return render(self.request, 'stripe/stripe.html', context)

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
            payment = Stripe()
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


class QiwiPayView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = order.get_qiwi_context()
        return render(self.request, "qiwi/qiwi.html", context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('')
        amount = int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token)

            # создаем объект платежа
            payment = Qiwi()
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

        except Exception as e:
            # Send an email to ourselves
            messages.error(self.request, "Произошла серьезная ошибка. Вам отправленно e-mail уведомление.")
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
        ordered=False)
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
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # проверяем если ордерный предмет в ордере
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]
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

@login_required
def redirect_home_payment_error(request):
    messages.error(request, "Ошибка в олате счета")
    return redirect('/')

@login_required
def redirect_home_payment_success(request):
    messages.success(request, "Ваш заказ оформлен успешно!")
    return redirect('/')



""" RobokassaViewClass
        # class RoboPaymentView(View):
        #     template_name = "payment/robokassa.html"

        #     def get(self, *args, **kwarg):
        #         # order
        #         order = Order.objects.get(user=self.request.user, ordered=False)
        #         form = RobokassaForm(initial={
        #             'MerchantLogin': 'bestboard',
        #             'Pass1': 'rOGKmIVFRbq9o6it01q7',
        #             'OutSum': '200',
        #             'InvId': '678678',
        #             # 'OutSum': int(order.get_total() * 100),
        #             # 'InvId': int(order.id),
        #             'Desc': str([item.item.title for item in order.items.all()]),
        #             'Email': self.request.user.email or 'user@example.com',
        #             'isTest': True,
        #             'Culture': 'ru'
        #         })

        #         return request('core:payment-robo', {"form": form})

        #     def post(self, *args, **kwargs):
        #         order = Order.objects.get(user=self.request.user, ordered=False)
        #         amount = int(order.get_total() * 100)

        #         try:
        #             # создаем объект платежа
        #             payment = Robo()
        #             payment.user = self.request.user
        #             payment.amount = order.get_total()
        #             payment.InvId = self.request.POST.get("InvId")
        #             payment.save()

        #             # назначить эту оплату этому заказу

        #             order_items = order.items.all()
        #             order_items.update(ordered=True)
        #             for item in order_items:
        #                 item.save()

        #             order.ordered = True
        #             order.payment = payment
        #             order.save()

        #             messages.success(self.request, "Ваш заказ оформлен успешно!")
        #             return redirect("/")

        #         except Exception as e:
        #             # Send an email to ourselves
        #             messages.error(self.request, "Произошла серьезная ошибка. Вам отправленно e-mail уведомление.")
        #             return redirect("/")


        # @login_required
        # def pay_with_robokassa(request):
        #     order = Order.objects.get(user=request.user, ordered=False)

        #     form = RobokassaForm(initial={
        #             'MerchantLogin': 'bestboard',
        #             'Pass1': 'rOGKmIVFRbq9o6it01q7',
        #             'OutSum': str(int(order.get_total() * 100)),
        #             'InvId': str(int(order.id)),
        #             'Desc': str([item.item.title for item in order.items.all()]),
        #             'isTest': 1,
        #             })

        #     robo_url = form.get_redirect_url()
        #     # return redirect(robo_url)
        #     return render(request, form.target, context)
"""