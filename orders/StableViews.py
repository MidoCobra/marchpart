from django.shortcuts import render, redirect
from .models import OrderItem, Order, ShippingCosts
from shop.models import Category, Product

from .forms import OrderCreateForm
from cart.cart import Cart

# from paypal.standard.forms import PayPalPaymentsForm
from decimal import Decimal
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings

# For paypal signals:
# from paypal.standard.models import ST_PP_COMPLETED, ST_PP_PENDING
# from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.dispatch import receiver

# from paypal.standard.ipn.models import PayPalIPN
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
import datetime

import requests
import hashlib
import hmac

from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


@login_required
def order_create(request):
    user = request.user
    cart = Cart(request)
    categories = Category.objects.all()
    shippings = ShippingCosts.objects.all().order_by("shipping_city")
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                # product_from_model = Product.objects.get(name=item['product'])
                # p_price = product_from_model.price
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    # price=p_price,
                    price=item["price"],
                    quantity=item["quantity"],
                )
            update_order = get_object_or_404(Order, id=order.id)
            update_order.fees = order.get_total_cost()
            update_order.user = user
            update_order.save()

            # update_order.delete_after_five_minutes
            # cart.clear()
        # return render(request, 'orders/order/created.html', {'order': order})
        # return HttpResponseRedirect(reverse('paynow',args=(kind,tour_id,buyer.id)))
        invoice_num = order.id
        return HttpResponseRedirect(reverse("orders:paynow", args=(invoice_num,)))
    else:

        form = OrderCreateForm()
    context = {
        "shippings": shippings,
        "form": form,
        "categories": categories,
    }
    return render(request, "orders/order/create.html", context)


@login_required
def order_create_arabic(request):
    user = request.user
    cart = Cart(request)
    categories = Category.objects.all()
    shippings = ShippingCosts.objects.all().order_by("shipping_city_arabic")
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                # product_from_model = Product.objects.get(name=item['product'])
                # p_price = product_from_model.price
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    # price=p_price,
                    price=item["price"],
                    quantity=item["quantity"],
                )
            update_order = get_object_or_404(Order, id=order.id)
            update_order.fees = order.get_total_cost()
            update_order.user = user
            update_order.save()
            print(datetime.datetime.now())
            # update_order.delete_after_five_minutes
            # cart.clear()
        # return render(request, 'orders/order/created.html', {'order': order})
        # return HttpResponseRedirect(reverse('paynow',args=(kind,tour_id,buyer.id)))
        invoice_num = order.id
        return HttpResponseRedirect(reverse("orders:paynow", args=(invoice_num,)))
    else:

        form = OrderCreateForm()
    context = {
        "shippings": shippings,
        "form": form,
        "categories": categories,
    }
    return render(request, "orders/order/create_arabic.html", context)


@login_required
def PayNow(request, invoice_num):
    cart = Cart(request)
    order = get_object_or_404(Order, id=invoice_num)
    order_city = order.city
    try:
        shipping = ShippingCosts.objects.get(shipping_city__iexact=order_city)
    except:
        try:
            shipping = ShippingCosts.objects.get(shipping_city_arabic__exact=order_city)
        except:
            return HttpResponse("Plese select a city from Available cities")
  
    shipping_price = shipping.shipping_cost

    # fees = cart.get_total_price() + shipping_price
    price_difference = None
    fees = order.get_total_cost()
    total_fees = fees + shipping_price

    if cart.get_total_price() != order.get_total_cost():
        price_difference_message = (
            "sorry Price Have Been Changed since Your Last Uncomplete order process"
        )
        price_difference = order.get_total_cost() - cart.get_total_price()

    invoice = invoice_num

    authentication_request_url = "https://accept.paymobsolutions.com/api/auth/tokens"
    order_registration_API_url = (
        "https://accept.paymobsolutions.com/api/ecommerce/orders"
    )
    payment_key_request_url = (
        "https://accept.paymobsolutions.com/api/acceptance/payment_keys"
    )

    auth_token = None
    r = requests.post(
        authentication_request_url,
        json={
            "api_key": "ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6VXhNaUo5LmV5SndjbTltYVd4bFgzQnJJam95TWpNNU5Dd2libUZ0WlNJNkltbHVhWFJwWVd3aUxDSmpiR0Z6Y3lJNklrMWxjbU5vWVc1MEluMC5xYmFCTTE0NUowT0V3Z1lrNVZXZ1U0eUtRVHVYeGJON2hxeklkUU0xeW9MOFQ1Ql8tYUNhNl9YX3J3SHExcFlQN0dYazRIaHRVbUNnRWU2aUU5TlpRQQ=="
        },
    )
    # print(r.content)
    status_code = r.status_code
    print("status code: " + str(status_code))
    print(r.json())

    auth_token = r.json()["token"]


    order_items = OrderItem.objects.filter(order=order)
    items = []
    for i in order_items:
        items.append(
            {
                "name": i.product.name,
                "amount_cents": int(i.price * 100),
                "quantity": i.quantity,
            }
        )

    print("items are: " + str(items))
    data = {
        "auth_token": auth_token,
        "delivery_needed": "false",
        "amount_cents": "100",
        "currency": "EGP",
        "merchant_order_id": str(
            invoice
        ),  # invoice  ########################################332
        "items": items,
        "shipping_data": {
            "apartment": "NA",
            "email": order.email,
            "floor": "42",
            "first_name": order.first_name,
            "street": order.address,
            "building": "NA",
            "phone_number": order.phone1,
            "postal_code": "NA",
            "city": order.city,
            "country": order.country,
            "last_name": order.last_name,
            "state": "NA",
        },
        # "shipping_details": {
        #     "notes": " test",
        #     "number_of_packages": 1,
        #     "weight": 1,
        #     "weight_unit": "Kilogram",
        #     "length": 1,
        #     "width": 1,
        #     "height": 1,
        #     "contents": "product of some sorts",
        # },
    }

    o = requests.post(order_registration_API_url, json=data)
    print("-----------------------------------------------")
    print("-----------------------------------------------")
    print("------------------Second Step-----------------------------")
    print("token: " + auth_token)
    print("============")
    print("second step: " + o.text)

    try:
        integration_id = o.json()["id"]
    except:
        return HttpResponse(
            "Duplicated Order Request!,  Please Go Back & Resend Your Order Request."
        )
    print("integration_id: " + str(o.json()["id"]))
    print("----------------------------------")
    print("----------------------------------")
    print("------------Third Step----------------------")

    params = {
        "auth_token": auth_token,
        "amount_cents": int(total_fees),  # total_fees
        "expiration": 3600,
        "order_id": integration_id,
        "billing_data": {
            "apartment": "NA",
            "email": "claudette09@exa.com",
            "floor": "42",
            "first_name": "Clifford",
            "street": "Ethan Land",
            "building": "8028",
            "phone_number": "+86(8)9135210487",
            "shipping_method": "PKG",
            "postal_code": "01898",
            "city": "Jaskolskiburgh",
            "country": "CR",
            "last_name": "Nicolas",
            "state": "NA",
        },
        "currency": "EGP",
        "integration_id": 46855,  ## production

        # "integration_id": 63588, ## Test Development
        "lock_order_when_paid": "false",
    }

    z = requests.post(payment_key_request_url, json=params)
    status_code2 = z.status_code
    print("status code_ last step >>> : " + str(status_code2))
    print("content_ last step >>> : " + z.text)
    print(z.json()["token"])

    payment_key = z.json()["token"]
    cart.clear()
    context = {
        "ship_fees": shipping_price,
        "fees": fees,
        "total_fees": total_fees,
        "price_difference": price_difference,
        "order": order,
        "cart": cart,
        "payment_key": payment_key,
    }
    return render(request, "orders/order/paynow.html", context)


def WeAcceptWalletView(request, payment_key):
    wallet_request_url = (
        "https://accept.paymobsolutions.com/api/acceptance/payments/pay"
    )
    data = {
        "source": {"identifier": "01010101010", "subtype": "WALLET"},
        "payment_token": payment_key,
    }
    r = requests.post(wallet_request_url, json=data)
    print("response==: " + r.text)
    wallet_url = r.json()["redirection_url"]
    context = {"wallet_url": wallet_url}
    return redirect(wallet_url)


def ProcessesCallback(request):
    order = Order.objects.get(id=38)
    order.paid = True
    order.save()
    if request.method == "GET":
        obj_integration_id = request.GET.get("obj:integration_id")
        print("object id = " + obj_integration_id)

        order = Order.objects.get(id=38)
        order.paid = True
        order.province = obj_integration_id
        order.save()
        return HttpResponse(obj_integration_id)
    return HttpResponse("response done")


def ResponseCallback(request):
    if request.method=="GET":
        amount_cents = request.GET.get("amount_cents")
        created_at= request.GET.get("created_at")
        currency = request.GET.get("currency")
        error_occured = request.GET.get("error_occured")
        has_parent_transaction = request.GET.get("has_parent_transaction")
        get_id = request.GET.get("id")
        integration_id = request.GET.get("integration_id")
        is_3d_secure = request.GET.get("is_3d_secure")
        is_auth = request.GET.get("is_auth")
        is_capture = request.GET.get("is_capture")
        is_refunded = request.GET.get("is_refunded")
        is_standalone_payment = request.GET.get("is_standalone_payment")
        is_voided = request.GET.get("is_voided")
        order = request.GET.get("order")
        owner = request.GET.get("owner")
        pending = request.GET.get("pending")
        source_data_pan = request.GET.get("source_data.pan")
        source_data_sub_type = request.GET.get("source_data.sub_type")
        source_data_type = request.GET.get("source_data.type")
        success = request.GET.get("success")
        get_hmac = request.GET.get("hmac")

        order_id = request.GET.get("merchant_order_id")

        data_message = request.GET.get("data.message")
        profile_id = request.GET.get("profile_id")
        is_refund = request.GET.get("is_refund")
        refunded_amount_cents = request.GET.get("refunded_amount_cents")
        captured_amount = request.GET.get("captured_amount")
        acq_response_code = request.GET.get("acq_response_code")
        txn_response_code = request.GET.get("txn_response_code")
        is_void = request.GET.get("is_void")


        # hmac_calculator_url = "https://accept.paymobsolutions.com/api/acceptance/transactions/"+ get_id +"/hmac_calc"
        # headers = {"Authorization": "Bearer ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmxlSEFpT2pFMk1ESTFPVFV4T0Rnc0luQnliMlpwYkdWZmNHc2lPakl5TXprMExDSmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljR2hoYzJnaU9pSm1Zak14TW1Sak1tRTROV0UwWXpaa016VTRNakUzTURRek1tWXhNV1EzTWpkbFptVTRZMkZqWmpZNVpqSmhPRGN6TVRaaE5UVm1OamsyTlRkbE4yRXhJbjAuQU9JS0NDbHc4VUZhLWJ5VzZuV3NTTkhYTXBGUjJ3czNVQ0lsbU1lU1VMRVgxZ0kxVnJ0blMzZHFqdVJOaEVWRFdXQzcxX3pzNERuMzRXRm1TRktJbUE=" }
        # # headers = {"Authorization": "Bearer " + auth_token}
        # r = requests.get(hmac_calculator_url, headers=headers)
        # print(r.text)
        # get_hmac_calc = r.json()["hmac"]
        # get_hmac_string =  r.json()['hmac_string']
        # print("hmac_calc string is= " +get_hmac_string)
        # hmac = amount_centscreated_atcurrencyerror_occuredhas_parent_transactionidintegration_idis_3d_secureis_authis_captureis_refundeis_standalone_paymentis_voidedorder.idownerpendingsource_data.pansource_data.sub_typesource_data.typesuccess
        # msg = (
        #     acq_response_code +
        #     amount_cents +
        #     captured_amount +
        #     created_at +
        #     currency +
        #     data_message +
        #     error_occured +
        #     has_parent_transaction +
        #     get_id +
        #     integration_id +
        #     is_3d_secure +
        #     is_auth +
        #     is_capture +
        #     is_refund +
        #     is_refunded +
        #     is_standalone_payment +
        #     is_void +
        #     is_voided +
        #     order +
        #     order_id +
        #     owner +
        #     pending +
        #     profile_id +
        #     refunded_amount_cents +
        #     source_data_pan +
        #     source_data_sub_type +
        #     source_data_type +
        #     success +
        #     txn_response_code 
        # )
        # msg_withHMAC = (
        #     "E980FF4BE16F9C7BD2DBE65A7FFAA667" +
        #     acq_response_code +
        #     amount_cents +
        #     captured_amount +
        #     created_at +
        #     currency +
        #     data_message +
        #     error_occured +
        #     has_parent_transaction +
        #     get_id +
        #     integration_id +
        #     is_3d_secure +
        #     is_auth +
        #     is_capture +
        #     is_refund +
        #     is_refunded +
        #     is_standalone_payment +
        #     is_void +
        #     is_voided +
        #     order +
        #     order_id +
        #     owner +
        #     pending +
        #     profile_id +
        #     refunded_amount_cents +
        #     source_data_pan +
        #     source_data_sub_type +
        #     source_data_type +
        #     success +
        #     txn_response_code 
            
        # )
        short_msg = (
            amount_cents +
            created_at +
            currency +
            error_occured +
            has_parent_transaction +
            get_id +
            integration_id +
            is_3d_secure +
            is_auth +
            is_capture +
            is_refunded +
            is_standalone_payment +
            is_voided +
            order +
            owner +
            pending +
            source_data_pan +
            source_data_sub_type +
            source_data_type +
            success
        )
        # short_msg_withHmac = (
        #     "E980FF4BE16F9C7BD2DBE65A7FFAA667" +
        #     amount_cents +
        #     created_at +
        #     currency +
        #     error_occured +
        #     has_parent_transaction +
        #     get_id +
        #     integration_id +
        #     is_3d_secure +
        #     is_auth +
        #     is_capture +
        #     is_refunded +
        #     is_standalone_payment +
        #     is_voided +
        #     order_id +
        #     owner +
        #     pending +
        #     source_data_pan +
        #     source_data_sub_type +
        #     source_data_type +
        #     success
            
        # )
        # hmac_digset = hashlib.sha512(
        #     get_hmac_string.encode()).hexdigest()

        # # hmac_digset = hashlib.sha512(
        # #     bytes(msg_withHMAC.lower(), 'utf-8')).hexdigest()
     

        # message = bytes(get_hmac_string, 'utf-8')
        # secret = bytes('E980FF4BE16F9C7BD2DBE65A7FFAA667', 'utf-8')
        # hash = hmac.new(secret, message, hashlib.sha512)
        # result = hash.hexdigest()

####################
        # short_hmac_digset = hashlib.sha512(
        #     short_msg_withHmac.lower().encode()).hexdigest()
        # # short_hmac_digset = hashlib.sha512(
        # #     bytes(short_msg_withHmac.lower(), 'utf-8')).hexdigest()

        message2 = bytes(short_msg, 'utf-8')
        secret = bytes('E980FF4BE16F9C7BD2DBE65A7FFAA667', 'utf-8')
        hashed = hmac.new(secret, message2, hashlib.sha512)
        short_result = hashed.hexdigest()

        # print("hmac_digest= "  + hmac_digset)
        # print("result= "  + result)
        # print("short_result= "  + short_result)


        # short_msg_inDetails = (
        #     amount_cents +
        #     created_at +
        #     currency +
        #     error_occured +
        #     has_parent_transaction +
        #     "get_id" +
        #     get_id +
        #     "integration_id" +
        #     integration_id +
        #     is_3d_secure +
        #     is_auth +
        #     is_capture +
        #     is_refunded +
        #     is_standalone_payment +
        #     "is_voided>> " +
        #     is_voided +
        #     "order_id>> " +
        #     order_id +
        #     "owner>> " +
        #     owner +
        #     "pending>> " +
        #     pending +
        #     source_data_pan +
        #     source_data_sub_type +
        #     source_data_type +
        #     success
        # )
        # print("short_msg_inDetails>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + short_msg_inDetails + "|||||")
        # print("short msg: >>> " + short_msg)
        # print("short_hmac_digset= "  + short_hmac_digset)



        if get_hmac == short_result:

            if success == "true":
    
                march_part_order = get_object_or_404(Order, id=order_id)
                print("marchpartOrder=  " + str(march_part_order))
                march_part_order.paid = True
                march_part_order.we_accept_transaction_id = get_id
                march_part_order.save()

                user = request.user
                order_items = OrderItem.objects.filter(order = march_part_order)
                current_site = get_current_site(request)
                subject = "Invoice"
                messageTest = render_to_string(
                    "orders/order/invoice.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        'fees' : march_part_order.fees,
                        'first_name' : march_part_order.first_name,
                        'last_name' : march_part_order.last_name,
                        'email' : march_part_order.email,
                        'user' : march_part_order.user,
                        'city' : march_part_order.city,
                        'address' : march_part_order.address,
                        'phone1' : march_part_order.phone1,
                        'phone2' : march_part_order.phone2,
                        'order_items' : order_items,
                    },
                )
                to_emails = [
                    (march_part_order.email),
                    ('m.desertcamel@gmail.com'),
                    ('mgmgbbnmichael5@gmail.com')
                ]
                # user.email_user(subject, message)
                # return redirect('account_activation_sent')
                message = Mail(
                    from_email=settings.FROM_EMAIL,
                    to_emails=to_emails,
                    subject=subject,
                    html_content=messageTest,
                )
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                sg.send(message)


                context = {
                    'fees' : march_part_order.fees,
                    'first_name' : march_part_order.first_name,
                    'last_name' : march_part_order.last_name,
                    'email' : march_part_order.email,
                    'user' : march_part_order.user,
                    'city' : march_part_order.city,
                    'address' : march_part_order.address,
                    'phone1' : march_part_order.phone1,
                    'phone2' : march_part_order.phone2,
                    'order_items' : order_items,
                }
                return render(request, 'success_payment.html', context)
            else:
                context={
                    'data_message' : data_message
                }
                return render(request, 'failed_payment.html', context)

    return render(request, 'home.html')