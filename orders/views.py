from django.shortcuts import render, redirect
from .models import OrderItem, Order, ShippingCosts, PromoCodes
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

from django.contrib import messages


@login_required
def order_create(request):
    user = request.user
    cart = Cart(request)
    categories = Category.objects.all()
    shippings = ShippingCosts.objects.all().order_by("shipping_city")
    net_fees = None
    coupon = None
    check_coupon = None
    wallet=None
    if request.method == "GET":
        coupon = request.GET.get("coupon", None)
        date = datetime.datetime.now()
        
        try:
            check_coupon = PromoCodes.objects.get(promo_code=coupon, valid_from__lte=date, valid_to__gte=date)
            # if check_coupon.valid_from <= date and check_coupon.valid_to >= date:
            calculate_discount = (cart.get_total_price() * int(check_coupon.discount_ratio)) / 100
            net_fees = int(cart.get_total_price()) - int(calculate_discount)
        except:
            if coupon is not None:
                messages.error(request, 'Invalid coupon number or expired one! check your coupon or just complete your order')

    
    if request.method == "POST":
        cashOnDelivery = request.POST.get('cashOnDelivery', None)
        wallet = request.POST.get('wallet', None)
        date = datetime.datetime.now()
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            if request.recaptcha_is_valid:
                if form.cleaned_data['city'] == None or form.cleaned_data['city'] == "none":
                    messages.error(request, "Please select city from list!")            
                elif not cart:
                    messages.error(request, "Your cart is empty! We cant't proceed your request. Please fill your cart first.")
                else:
                    order = form.save()
                   
                #    Want to Get the price from database here not from the cart
                  
                    # for item in cart:
                    #     # product_from_model = Product.objects.get(name=item['product'])
                    #     # p_price = product_from_model.price
                    #     cart.update(product=item["product"], quantity= item["quantity"])
                    #     # cart.save()
                    for item in cart:
                        if (Product.objects.get(name=item["product"])).sale_price == None or (Product.objects.get(name=item["product"])).sale_price == 0:
                            OrderItem.objects.create(
                                order=order,
                                product=item["product"],
                                # price=p_price,
                                price = ((Product.objects.get(name=item["product"])).price),
                                quantity=item["quantity"],
                            )
                            print(" Price is: "  + str((Product.objects.get(name=item["product"])).price))
                        else: 
                            OrderItem.objects.create(
                                order=order,
                                product=item["product"],
                                # price=p_price,
                                price = ((Product.objects.get(name=item["product"])).sale_price),
                                quantity=item["quantity"],
                            )
                            print("Sale Price Is :" + str((Product.objects.get(name=item["product"])).sale_price))
                    # order_items = OrderItem.objects.filter(order=order)
                    # for item in order_items:
                    #     order_items.update(price=)     

                    update_order = get_object_or_404(Order, id=order.id)
                    update_order.user = user
                    # if order.promo_code != None:
                    try:
                        check_coupon = PromoCodes.objects.get(promo_code=order.promo_code, valid_from__lte=date, valid_to__gte=date)
                        # if check_coupon.valid_from <= date and check_coupon.valid_to >= date:
                        calculate_discount = (order.get_total_cost() * int(check_coupon.discount_ratio)) / 100
                        net_fees = int(order.get_total_cost()) - int(calculate_discount)
                        print("net_fees is not None")
                        update_order.fees = net_fees
                        update_order.price_before_promo_code = order.get_total_cost()
                        update_order.promo_code = check_coupon.pormotionName
                    except:
                    #     # messages.error(request, 'Invalid coupon number or expired one!')
                    #     pass
                    # else: 
                        print("normal cost")
                        update_order.fees = update_order.get_total_cost()
                        # update_order.fees = int(cart.get_total_price())
                        update_order.promo_code = "No Promo Code"
                    update_order.save()

                    # update_order.delete_after_five_minutes
                    # cart.clear()
                # return render(request, 'orders/order/created.html', {'order': order})
                # return HttpResponseRedirect(reverse('paynow',args=(kind,tour_id,buyer.id)))
                    # if update_order.city == None:
                    #     messages.error(request, "Please select city from list!")
                    if update_order.fees == 0 or update_order.fees == None:
                        messages.error(request, "Your cart is empty! We cant't proceed your request.")
                        # update_order.delete()
                    else:
                        invoice_num = order.code
                        order_fees = int(update_order.fees)
                        total_fees = None
                        paid_shipping = None
                        shipping = ShippingCosts.objects.get(shipping_city__iexact=update_order.city)
                        shipping_price = shipping.shipping_cost
                        free_shipping_product = Order.objects.filter(id= update_order.id, items__product__free_shipping=True)

                        if free_shipping_product:
                            total_fees = order_fees
                        else:
                            if order_fees <= 1000:
                                total_fees = int(order_fees + shipping_price)
                                paid_shipping = shipping_price
                                update_order.shipping_fees = paid_shipping
                            else:
                                total_fees = order_fees
                        update_order.fees = total_fees
                        update_order.save()
                        # update_order.fees = update_order.get_total_cost() + int(shipping_price)
                        if cashOnDelivery:
                            update_order.cashOnDelivery = True
                            update_order.save()
                            order_items = OrderItem.objects.filter(order = update_order)
                            cart.clear()
                            current_site = get_current_site(request)
                            subject = "Invoice"
                            messageTest = render_to_string(
                                "orders/order/order-email.html",
                                {
                                    "domain": current_site.domain,
                                    'fees' : update_order.fees,
                                    'first_name' : update_order.first_name,
                                    'last_name' : update_order.last_name,
                                    'email' : update_order.email,
                                    'user' : update_order.user,
                                    'city' : update_order.city,
                                    'address' : update_order.address,
                                    'phone1' : update_order.phone1,
                                    'phone2' : update_order.phone2,
                                    'invoice' : update_order.code,
                                    'order_items' : order_items,
                                    'shipping' : update_order.shipping_fees,
                                },
                            )
                            to_emails = [
                                (update_order.email),
                                ('m.desertcamel@gmail.com'),
                                ('mgmgbbnmichael5@gmail.com')
                            ]
                            message = Mail(
                                from_email=settings.FROM_EMAIL,
                                to_emails=to_emails,
                                subject=subject,
                                html_content=messageTest,
                            )
                            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                            sg.send(message)
                            context = {
                                'order' : update_order,
                                'order_items' : order_items,
                            }
                            return render(request, 'cash-on-delivery.html', context)
                        else:
                            # cart.clear()
                            return HttpResponseRedirect(reverse("orders:paynow", args=(invoice_num,wallet,"shop/base.html")))

    else:

        form = OrderCreateForm()
    context = {
        "shippings": shippings,
        "form": form,
        "categories": categories,
        "net_fees": net_fees,
        "coupon": coupon,
    }
    return render(request, "orders/order/create.html", context)


@login_required
def order_create_arabic(request):
    user = request.user
    cart = Cart(request)
    categories = Category.objects.all()
    shippings = ShippingCosts.objects.all().order_by("shipping_city_arabic")
    net_fees = None
    coupon = None
    check_coupon = None  
    wallet=None
    if request.method == "GET":
        coupon = request.GET.get("coupon", None)
        date = datetime.datetime.now()
        
        try:
            check_coupon = PromoCodes.objects.get(promo_code=coupon, valid_from__lte=date, valid_to__gte=date)
            # if check_coupon.valid_from <= date and check_coupon.valid_to >= date:
            calculate_discount = (cart.get_total_price() * int(check_coupon.discount_ratio)) / 100
            net_fees = int(cart.get_total_price()) - int(calculate_discount)
        except:
            if coupon is not None:
                messages.error(request, 'الكوبون المسخدم غير صحيح او منتهى الصلاحية، يمكنك الرجوع للتأكد أو استكمال عملية الحجز دون الخروج من الصفحة')

      
    if request.method == "POST":
        cashOnDelivery = request.POST.get('cashOnDelivery', None)
        wallet = request.POST.get('wallet', None)
        date = datetime.datetime.now()
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            if request.recaptcha_is_valid:
                if form.cleaned_data['city'] == None or form.cleaned_data['city'] == "none":
                    messages.error(request, "من فضلك اختر مدينة من القائمة")            
                elif not cart:
                    messages.error(request, "عربة التسوق خاليه، لا يمكن اتمام العمليه بدون وجود منتجات")
                else:
                    order = form.save()
                    for item in cart:
                        # product_from_model = Product.objects.get(name=item['product'])
                        # p_price = product_from_model.price
                        cart.update(product=item["product"], quantity= item["quantity"])
                        cart.save()
                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item["product"],
                            # price=p_price,
                            price=item["price"],
                            quantity=item["quantity"],
                        )
                    update_order = get_object_or_404(Order, id=order.id)
                    update_order.user = user
                    
                    # if order.promo_code != None:
                    try:
                        check_coupon = PromoCodes.objects.get(promo_code=order.promo_code, valid_from__lte=date, valid_to__gte=date)
                        # if check_coupon.valid_from <= date and check_coupon.valid_to >= date:
                        calculate_discount = (cart.get_total_price() * int(check_coupon.discount_ratio)) / 100
                        net_fees = int(cart.get_total_price()) - int(calculate_discount)
                        print("net_fees is not None")
                        update_order.fees = net_fees
                        update_order.price_before_promo_code = order.get_total_cost()
                        update_order.promo_code = check_coupon.pormotionName
                        update_order.save()
                    except:
                    #     # messages.error(request, 'Invalid coupon number or expired one!')
                    #     pass
                    # else: 
                        print("normal cost")
                        update_order.fees = order.get_total_cost()
                        update_order.promo_code = "No Promo Code"
                        update_order.save()

                    # update_order.delete_after_five_minutes
                    # cart.clear()
                # return render(request, 'orders/order/created.html', {'order': order})
                # return HttpResponseRedirect(reverse('paynow',args=(kind,tour_id,buyer.id)))
                    # if update_order.city == None:
                    #     messages.error(request, "Please select city from list!")
                    if update_order.fees == 0 or update_order.fees == None:
                        messages.error(request, "لا يوجد منتجات بعربة التسوق الخاصة بك")
                        # update_order.delete()
                    else:
                        invoice_num = order.code
                        paid_shipping = None

                        order_fees = int(update_order.fees)
                        total_fees = None
                        shipping = ShippingCosts.objects.get(shipping_city_arabic__exact=update_order.city)
                        shipping_price = shipping.shipping_cost
                        if order_fees <= 1000:
                            total_fees = int(order_fees + shipping_price)
                            paid_shipping = shipping_price
                        else:
                            total_fees = order_fees
                        update_order.fees = total_fees
                        update_order.shipping_fees = paid_shipping
                        update_order.save()

                        if cashOnDelivery:
                            update_order.cashOnDelivery = True
                            update_order.save()
                            order_items = OrderItem.objects.filter(order = update_order)
                            cart.clear()
                            current_site = get_current_site(request)
                            subject = "Invoice"
                            messageTest = render_to_string(
                                "orders/order/order-email.html",
                                {
                                    "domain": current_site.domain,
                                    'fees' : update_order.fees,
                                    'first_name' : update_order.first_name,
                                    'last_name' : update_order.last_name,
                                    'email' : update_order.email,
                                    'user' : update_order.user,
                                    'city' : update_order.city,
                                    'address' : update_order.address,
                                    'phone1' : update_order.phone1,
                                    'phone2' : update_order.phone2,
                                    'invoice' : update_order.code,
                                    'order_items' : order_items,
                                    'shipping' : update_order.shipping_fees,
                                },
                            )
                            to_emails = [
                                (update_order.email),
                                ('m.desertcamel@gmail.com'),
                                ('mgmgbbnmichael5@gmail.com')
                            ]
                            message = Mail(
                                from_email=settings.FROM_EMAIL,
                                to_emails=to_emails,
                                subject=subject,
                                html_content=messageTest,
                            )
                            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                            sg.send(message)
                            context = {
                                'order' : update_order,
                                'order_items' : order_items,
                            }

                            return render(request, 'cash-on-delivery-arabic.html', context)
                        else: 
                            cart.clear()                                                     
                            return HttpResponseRedirect(reverse("orders:paynow", args=(invoice_num, wallet,"shop_arabic/base_arabic.html")))
                       
        else:
            # return HttpResponse('Form is not valid')
            messages.error(request, "Error")
    else:

        form = OrderCreateForm()
    context = {
        "shippings": shippings,
        "form": form,
        "categories": categories,
        "net_fees": net_fees,
        "coupon": coupon,
    }
    return render(request, "orders/order/create_arabic.html", context)


# @login_required
def PayNow(request, invoice_num, wallet, language):
    cart = Cart(request)
    order = get_object_or_404(Order, code=invoice_num)
    order_city = order.city
    wallet=wallet
    language=language
    shipping_price = 0
    calculate_discount = None
    
    ## Will Add filter as a sainty check for paid orders to give an error or fake order error
    ## Or may be paid order normally will return duplicate error
    # This Is for request from mobile applications:
    date = datetime.datetime.now()
    print ("Order Promo code = "+ order.promo_code)
    print ("Order price_before_promo_code = "+ order.price_before_promo_code)
    print ("Order order.get_total_cost() = "+ str(order.get_total_cost()))

    try:
        check_coupon = PromoCodes.objects.get(pormotionName=order.promo_code, valid_from__lte=date, valid_to__gte=date)
        # if check_coupon.valid_from <= date and check_coupon.valid_to >= date:
        calculate_discount = (order.get_total_cost() * int(check_coupon.discount_ratio)) / 100
        order.price_before_promo_code = order.get_total_cost()
        net_fees = int(order.get_total_cost()) - int(calculate_discount)
        order.fees = net_fees
        order.promo_code = check_coupon.pormotionName
        print (">>>>>>>>>>>>>>> Order Promo Code Accepted")
    except:
        print("normal cost online payment")
        order.fees = order.get_total_cost()
        # update_order.fees = int(cart.get_total_price())
        order.promo_code = "No Promo Code"
    order.save()
    order_fees = order.fees
    print(order_city)
    try:
        shipping = ShippingCosts.objects.get(shipping_city__iexact=order_city)
        shipping_price = shipping.shipping_cost
        if order_fees <= 1000:
            total_fees = int(order_fees + shipping_price)
            order.fees = total_fees
            order.shipping_fees = shipping_price
            order.save()    
        else:
            total_fees = order_fees
            order.fees = total_fees
            shipping_price = 0
            order.save()

    except:
        try:
            shipping = ShippingCosts.objects.get(shipping_city_arabic__exact=order_city)
            shipping_price = shipping.shipping_cost
            if order_fees <= 1000:
                total_fees = int(order_fees + shipping_price)
                order.fees = total_fees
                order.shipping_fees = shipping_price
                order.save()
            else:
                total_fees = order_fees
                order.fees = total_fees
                shipping_price = 0
                order.save()
        except:
            return HttpResponse("Plese select a city from Available cities ... (Before Payment Check) ")
    """ get products prices from the product model """
    # order_items = OrderItem.objects.filter(order=order)
    # get_product = order_items.product.price
    

    # # fees = cart.get_total_price() + shipping_price
    # price_difference = None
    # fees = order.get_total_cost()

    # # get_promo = order.promoCode
    # # check_promos = PromoCodes.objects.filter(promo_code=get_promo)
    # total_fees = None
    # if fees <= 1000:
    #     total_fees = fees + shipping_price
    # else:
    #     total_fees = fees

    # if cart.get_total_price() != order.get_total_cost():
    #     price_difference_message = (
    #         "sorry Price Have Been Changed since Your Last Uncomplete order process"
    #     )
    #     price_difference = order.get_total_cost() - cart.get_total_price()


    # total_fees = order.fees



    # total_fees = order.get_total_cost() + int(shipping_price) ### old version before mobile app
# Also Removed this after handling the total_fees in the try except in the same view
    # if order.fees <= 1000:
    #     total_fees = order.fees + int(shipping_price)
    # else:
    #     total_fees = order.fees
 
    ### Sainty check:
    print('Total Fees to be sent to paymob is:' + str(total_fees))

    # invoice = invoice_num  ### i m trying to change this for non duplication gonna track the errors
    invoice= order.code
########################################## APIs URLs ########################################## 

    authentication_request_url = "https://accept.paymobsolutions.com/api/auth/tokens"
    order_registration_API_url = (
        "https://accept.paymobsolutions.com/api/ecommerce/orders"
    )
    payment_key_request_url = (
        "https://accept.paymobsolutions.com/api/acceptance/payment_keys"
    )


########################################## First Step ##########################################
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

########################################## Second Step ##########################################
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
        "amount_cents": int(total_fees),
        "currency": "EGP",
        "merchant_order_id": str(
            invoice
        ),
        "items": items,
        "shipping_data": {
            "apartment": "NA",
            "email": order.email,
            "floor": "NA",
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
        requested_integration_order_id = o.json()["id"]
    except:
        return HttpResponse(
            "Duplicated Order Request!,  Please Go Back & Refresh Order Request."
        )
    print("requested_integration_order_id: " + str(o.json()["id"]))
    print("----------------------------------")
    print("----------------------------------")
    print("------------Third Step----------------------")

########################################## Third Step ##########################################
    if wallet == 'None':
        params = {
            "auth_token": auth_token,
            "amount_cents": int(total_fees) * 100,  # total_fees
            "expiration": 3600,
            "order_id": requested_integration_order_id,
            "billing_data": {
                "apartment": "NA",
                "email": "NA",
                "floor": "NA",
                "first_name": "NA",
                "street": "NA",
                "building": "NA",
                "phone_number": "NA",
                "shipping_method": "NA",
                "postal_code": "NA",
                "city": "NA",
                "country": "NA",
                "last_name": "NA",
                "state": "NA",
            },
            "currency": "EGP",
            # "integration_id": 46855,  ############################# test production

            "integration_id": 123468, ########################### live production

            # "integration_id": 72952, ########################### Test wallet Development
            "lock_order_when_paid": "false",
        }
    else:    
        params = {
            "auth_token": auth_token,
            "amount_cents": int(total_fees) * 100,  # total_fees
            "expiration": 3600,
            "order_id": requested_integration_order_id,
            "billing_data": {
                "apartment": "NA",
                "email": "NA",
                "floor": "NA",
                "first_name": "NA",
                "street": "NA",
                "building": "NA",
                "phone_number": "NA",
                "shipping_method": "NA",
                "postal_code": "NA",
                "city": "NA",
                "country": "NA",
                "last_name": "NA",
                "state": "NA",
            },
            "currency": "EGP",
            # "integration_id": 46855,  ############################# test develpoment
            "integration_id": 123467, ########################### live wallet Development
            # "integration_id": 72952, ########################### Test wallet Development
            "lock_order_when_paid": "false",
        }

    z = requests.post(payment_key_request_url, json=params)
    status_code2 = z.status_code
    print('integration_id ...............................:   '  + str(params['integration_id']))
    print('wallet = ' + wallet)
    print("status code_ last step >>> : " + str(status_code2))
    print("content_ last step >>> : " + z.text)
    print(z.json()["token"])

    payment_key = z.json()["token"]
    cart.clear()
    context = {
        "ship_fees": shipping_price,
        # "fees": fees,
        "total_fees": total_fees,
        # "price_difference": price_difference,
        "order": order,
        "cart": cart,
        "payment_key": payment_key,
        "wallet": wallet,
        "language": language,
        "calculate_discount": calculate_discount,
    }
    return render(request, "orders/order/paynow.html", context)


def MobileWallet(request, payment_key):
    if request.method == "POST":
        identifier = request.POST.get("mobile")
        print("identifier = " + identifier)
        url = " https://accept.paymobsolutions.com/api/acceptance/payments/pay"
        data = {
            "source": {
                "identifier": identifier, 
                "subtype": "WALLET"
            },
            "payment_token": payment_key 
            }
        r = requests.post(url, json=data)

        print(r.text)
        wallet_url = r.json()["redirect_url"]
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

        message2 = bytes(short_msg, 'utf-8')
        secret = bytes('E980FF4BE16F9C7BD2DBE65A7FFAA667', 'utf-8')
        hashed = hmac.new(secret, message2, hashlib.sha512)
        short_result = hashed.hexdigest()
   
        if get_hmac == short_result:
            if success == "true": 
                march_part_order=get_object_or_404(Order, code=order_id)
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
                        "domain": current_site.domain,
                        'shipping' : march_part_order.shipping_fees,
                        'fees' : march_part_order.fees,
                        'invoice' : march_part_order.code,
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
                    'invoice' : march_part_order.code,
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