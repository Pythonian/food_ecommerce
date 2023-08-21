from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.conf import settings

from carts.cart import Cart
from accounts.models import LecturerPreference
from products.models import Product

from .models import OrderItem, Order
from .forms import OrderCreateForm


# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             if request.user.is_authenticated:
#                 order.user = request.user
#             order.save()
#             request.session['order_id'] = order.id

#             for item in cart:
#                 if request.user.is_authenticated:
#                     OrderItem.objects.create(
#                         order=order,
#                         product=item['product'],
#                         price=item['price'],
#                         user=request.user,
#                         vendor=item['product'].vendor.vendor,
#                         quantity=item['quantity'])
#                     order.vendors.add(item['product'].vendor.vendor)

#                 else:
#                     OrderItem.objects.create(
#                         order=order,
#                         product=item['product'],
#                         price=item['price'],
#                         vendor=item['product'].vendor.vendor,
#                         quantity=item['quantity'])
#                     order.vendors.add(item['product'].vendor.vendor)

#             # clear the cart
#             cart.clear()
#             return render(request,
#                           'orders/created.html',
#                           {'order': order})
#     else:
#         form = OrderCreateForm()
#         if request.user.is_authenticated:
#             initial_data = {
#                 'first_name': request.user.first_name,
#                 'last_name': request.user.last_name,
#                 'email': request.user.email,
#                 'address': request.user.customer.address,
#                 'phone_number': request.user.customer.phone_number,
#             }
#             form = OrderCreateForm(initial=initial_data)
#     return render(request,
#                   'orders/create.html',
#                   {'cart': cart, 'form': form})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            request.session['order_id'] = order.id

            total_calories = 0
            total_protein = 0
            total_carbohydrates = 0
            total_fats = 0
            total_vitamins = 0
            total_minerals = 0
            total_fiber = 0

            for item in cart:
                product = item['product']
                quantity = item['quantity']

                total_calories += product.calories * quantity
                total_protein += product.protein * quantity
                total_carbohydrates += product.carbohydrates * quantity
                total_fats += product.fats * quantity
                total_vitamins += product.vitamins * quantity
                total_minerals += product.minerals * quantity
                total_fiber += product.fiber * quantity

                if request.user.is_authenticated:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=item['price'],
                        user=request.user,
                        vendor=product.vendor.vendor,
                        quantity=quantity)
                    order.vendors.add(product.vendor.vendor)
                else:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=item['price'],
                        vendor=product.vendor.vendor,
                        quantity=quantity)
                    order.vendors.add(product.vendor.vendor)

            lecturer = request.user.customer
            preference, created = LecturerPreference.objects.get_or_create(lecturer=lecturer)

            # Convert preferred_calories to an integer
            preferred_calories = int(preference.preferred_calories) if preference.preferred_calories else 0
            preferred_protein = int(preference.preferred_protein) if preference.preferred_protein else 0
            preferred_carbohydrates = int(preference.preferred_carbohydrates) if preference.preferred_carbohydrates else 0
            preferred_fats = int(preference.preferred_fats) if preference.preferred_fats else 0
            preferred_vitamins = int(preference.preferred_vitamins) if preference.preferred_vitamins else 0
            preferred_minerals = int(preference.preferred_minerals) if preference.preferred_minerals else 0
            preferred_fiber = int(preference.preferred_fiber) if preference.preferred_fiber else 0

            
            # Update lecturer's nutritional preferences based on the ordered food items
            preference.preferred_calories = (preferred_calories + total_calories) // 2
            preference.preferred_protein = (preferred_protein + total_protein) // 2
            preference.preferred_carbohydrates = (preferred_carbohydrates + total_carbohydrates) // 2
            preference.preferred_fats = (preferred_fats + total_fats) // 2
            preference.preferred_vitamins = (preferred_vitamins + total_vitamins) // 2
            preference.preferred_minerals = (preferred_minerals + total_minerals) // 2
            preference.preferred_fiber = (preferred_fiber + total_fiber) // 2
            preference.save()

            # Clear the cart
            cart.clear()
            return render(request,
                          'orders/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'address': request.user.customer.address,
                'phone_number': request.user.customer.phone_number,
            }
            form = OrderCreateForm(initial=initial_data)
    return render(request,
                  'orders/create.html',
                  {'cart': cart, 'form': form})


@login_required
def confirm_order(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(order, id=order_id)

    paystack_amount = int(order.get_total_cost * 100)
    paystack_ref = None
    if not paystack_ref:
        paystack_ref = get_random_string(length=12).upper()
        order.paystack_id = paystack_ref
        order.total_amount = order.get_total_cost
        order.save()
    paystack_redirect_url = "{}?amount={}".format(
        reverse('paystack:verify_payment',
                args=[paystack_ref]), paystack_amount, order)

    template = 'orders/confirm_order.html'
    context = {'order': order,
                   'paystack_key': settings.PAYSTACK_PUBLIC_KEY,
                   'paystack_amount': paystack_amount,
                   'paystack_redirect_url': paystack_redirect_url
    }
    return render(request, template, context)


@csrf_exempt
def payment_done(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(order, id=order_id)
    return render(request, 'orders/invoice.html', {'order': order})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'orders/canceled.html')


@login_required
def track_order(request, id):
    order = get_object_or_404(Order, id=id)

    return render(
        request, 'orders/track_order.html', {'order': order})


@login_required
def order_status_shipped(request, id):
    order = get_object_or_404(Order, id=id)
    current_url = request.META['HTTP_REFERER']
    order.status = order.SHIPPED
    order.save()
    # send mail to user to inform him/her of change in order status
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = order.email
    send_mail(
        'Order status information',
        'Hi there, your order status has been changed to: SHIPPED',
        from_email,
        [to_email],
        fail_silently=False
    )
    messages.success(
        request, "Order status changed to: Shipped")
    return redirect(current_url)


@login_required
def order_status_processing(request, id):
    order = get_object_or_404(Order, id=id)
    current_url = request.META['HTTP_REFERER']
    order.status = order.PROCESSING
    order.save()
    # send mail to user to inform him/her of change in order status
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = order.email
    send_mail(
        'Order status information',
        'Hi there, your order status has been changed to: PROCESSING',
        from_email,
        [to_email],
        fail_silently=False
    )
    messages.success(
        request, "Order status changed to: Processing")
    return redirect(current_url)


@login_required
def order_status_completed(request, id):
    order = get_object_or_404(Order, id=id)
    current_url = request.META['HTTP_REFERER']
    order.status = order.COMPLETED
    order.save()
    # send mail to user to inform him/her of change in order status
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = order.email
    send_mail(
        'Order status information',
        'Hi there, your order has successfully been completed.',
        from_email,
        [to_email],
        fail_silently=False
    )
    messages.success(
        request, "Order status changed to: Completed")
    return redirect(current_url)
