from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import JsonResponse
from .forms import CustomUserCreationForm, UpdateAccountForm, LoginArabicForm

# For email verification
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from users.tokens import account_activation_token

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Tryin customuser instead of User:
from .models import CustomUser
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

###################### Dashboard #################
from django.contrib.auth.decorators import login_required


import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import hashlib
from datetime import date

from shop.models import Product
from orders.models import Order, OrderItem
from .models import Wishlist

from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if request.recaptcha_is_valid:
                user = form.save(commit=False)
                user.is_active = False
                # I add recaptcha!!

                user.save()
                current_site = get_current_site(request)
                subject = "Activate March Parts Account"
                messageTest = render_to_string(
                    "account_activation_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    },
                )
                # user.email_user(subject, message)
                # return redirect('account_activation_sent')
                message = Mail(
                    from_email=settings.FROM_EMAIL,
                    to_emails=user.email,
                    subject=subject,
                    html_content=messageTest,
                )
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                sg.send(message)
                return redirect("account_activation_sent")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


def account_activation_sent(request):
    return render(request, "account_activation_sent.html")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("shop_arabic:home_arabic")
    else:
        return render(request, "account_activation_invalid.html")


def validate_username(request):
    username = request.GET.get("username", None)
    data = {"is_taken": CustomUser.objects.filter(username__iexact=username).exists()}
    if data["is_taken"]:
        data["error_message"] = "Username Already Taken"
    return JsonResponse(data)


def validate_email(request):
    email = request.GET.get("email", None)
    data = {"is_taken": CustomUser.objects.filter(email__iexact=email).exists()}
    if data["is_taken"]:
        data["error_message"] = "An Account With This Email Already Exists!"
    return JsonResponse(data)


def UpdateAccount(request):
    user = request.user
    customUser = get_object_or_404(CustomUser, id=user.id)
    if request.method == "POST":
        form = UpdateAccountForm(request.POST or None, instance=customUser)
        if form.is_valid():
            # if request.recaptcha_is_valid:
            form.save()
            return render(request, "/")

    else:
        # For Security remove this
        form = UpdateAccountForm(request.POST or None, instance=customUser)

    context = {
        "form": form,
    }
    return render(request, "users/update.html", context)


def password_reset_request(request):
    protocol = "https://" if request.is_secure() else "http://"
    web_url = protocol + request.get_host()
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.html"
                    c = {
                        "email": user.email,
                        "domain": request.get_host(),
                        "site_name": "Website",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "https" if request.is_secure() else "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        to_emails = [
                            (user.email),
                        ]
                        message = Mail(
                            from_email= settings.FROM_EMAIL,
                            to_emails= to_emails,
                            subject= subject,
                            html_content=email
                        )
                        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                        sg.send(message)
                        # send_mail(
                        #     subject,
                        #     email,
                        #     "contact@marchpart.com",
                        #     [user.email],
                        #     fail_silently=False,
                        # )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect(web_url + "/accounts/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="password_reset_form.html",
        context={"form": password_reset_form},
    )


###########################################################################################################
###########################################################################################################
###########################################################################################################


@login_required(login_url="login")
def UserDashboard(request, id):
    user = request.user
    if user.id == id:
        customUser = get_object_or_404(CustomUser, id=user.id)
        if request.method == "POST":
            form = UpdateAccountForm(request.POST or None, instance=customUser)
            if form.is_valid():
                # if request.recaptcha_is_valid:
                form.save()
                return render(request, "shop/product/home.html")

        else:
            # For Security remove this
            form = UpdateAccountForm(request.POST or None, instance=customUser)

        context = {
            "form": form,
            "user": user,
        }
        return render(request, "users/user_home.html", context)
    else:
        return HttpResponse('Do Not Do This!')
    return HttpResponse('Nothing to see') 


@csrf_exempt
def Ajax_Wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    wishlist = Wishlist()
    wishlist.product = product
    wishlist.get_user = user
    response_data = {}
    if Wishlist.objects.filter(product=product, get_user=user).exists():
        response_data["already_added"] = "already_added"
        return JsonResponse(response_data)

        # messages.info(request,'Already added... Check Your own page.')
    else:
        wishlist.save()
        response_data["product_added"] = "product_added"
        return JsonResponse(response_data)
        # messages.success(request,'Tour added successfully to your wishlist.. Check Your own page. ')
    # return HttpResponseRedirect(reverse('tourdetails', args=(tour.id,)))


def RemoveFromWishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    wishlist_item = Wishlist.objects.get(product_id=product_id, get_user=user)

    wishlist_item.delete()
    return HttpResponseRedirect(reverse("wishlistView", args=(user.id,)))


def WishlistView(request, user_id):
    user = request.user
    if user.id == user_id:
        wishlist = Wishlist.objects.filter(get_user_id=user_id)
        context = {"wishlist": wishlist}
        return render(request, "users/wishlist.html", context)
    else:
        return HttpResponse('Do Not Do This!')
    return HttpResponse('Nothing to see') 


def UserInvoices(request):
    user = request.user
    if user:
        paidInvoices = Order.objects.filter(user_id=user.id, paid=True)
        cashOnDeliveryInvoice = Order.objects.filter(user_id=user.id, paid=False, cashOnDelivery=True)
        order_items = OrderItem.objects.all()
        context = {
            "paidInvoices": paidInvoices,
            "cashOnDeliveryInvoice": cashOnDeliveryInvoice,
            "order_items": order_items,
            }
        return render(request, "users/user-invoices.html", context)
    else:
        return HttpResponse('Do Not Do This!')
    return HttpResponse('Nothing to see') 





# def UpgradeToVIP(request, id):
#     user =  get_object_or_404(CustomUser, id=id)
#     user.is_vip = True
#     user.save()

#     return render(request, 'home.html')


################################################### اللغة العربية  ################## اللغة العربية
################################################### اللغة العربية ################## اللغة العربية


def Login_arabic(request):
    form = LoginArabicForm
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('shop_arabic:home_arabic')
        else:
            # Return an 'invalid login' error message.
            pass
    context = {"form": form}
    return render(request, "registration/login_arabic.html", context)


def signup_arabic(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if request.recaptcha_is_valid:
                user = form.save(commit=False)
                user.is_active = False
                # I add recaptcha!!

                user.save()
                current_site = get_current_site(request)
                subject = "Activate March Parts Account"
                messageTest = render_to_string(
                    "account_activation_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    },
                )
                # user.email_user(subject, message)
                # return redirect('account_activation_sent')
                message = Mail(
                    from_email=settings.FROM_EMAIL,
                    to_emails=user.email,
                    subject=subject,
                    html_content=messageTest,
                )
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                sg.send(message)
                return redirect("account_activation_sent")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup_arabic.html", {"form": form})


@login_required(login_url="login")
def UserDashboard_arabic(request, id):
    user = request.user
    customUser = get_object_or_404(CustomUser, id=user.id)
    if request.method == "POST":
        form = UpdateAccountForm(request.POST or None, instance=customUser)
        if form.is_valid():
            # if request.recaptcha_is_valid:
            form.save()
            return render(request, "shop_arabic/product_arabic/home_arabic.html")

    else:
        # For Security remove this
        form = UpdateAccountForm(request.POST or None, instance=customUser)

    context = {
        "form": form,
        "user": user,
    }
    return render(request, "users/user_home_arabic.html", context)


def RemoveFromWishlist_arabic(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    wishlist_item = Wishlist.objects.get(product_id=product_id, get_user=user)

    wishlist_item.delete()
    return HttpResponseRedirect(reverse("wishlistView_arabic", args=(user.id,)))


def WishlistView_arabic(request, user_id):
    user = request.user
    wishlist = Wishlist.objects.filter(get_user_id=user_id)
    context = {"wishlist": wishlist}
    return render(request, "users/wishlist_arabic.html", context)



def UserInvoices_arabic(request):
    user = request.user
    if user:
        paidInvoices = Order.objects.filter(user_id=user.id, paid=True)
        cashOnDeliveryInvoice = Order.objects.filter(user_id=user.id, paid=False, cashOnDelivery=True)
        order_items = OrderItem.objects.all()
        context = {
            "paidInvoices": paidInvoices,
            "cashOnDeliveryInvoice": cashOnDeliveryInvoice,
            "order_items": order_items,
            }
        return render(request, "users/user-invoices_arabic.html", context)
    else:
        return HttpResponse('Do Not Do This!')
    return HttpResponse('Nothing to see') 

################################################### اللغة العربية النهاية  ############## اللغة العربية النهاية
################################################### اللغة العربية النهاية  ############## اللغة العربية النهاية


##################################  SIGNUP MOBILE APPLICATION #############################
##################################  SIGNUP MOBILE APPLICATION #############################
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def Signup_Mobile_App(request, api_key):
    user = CustomUser
    if api_key == "test-key":
        pass

