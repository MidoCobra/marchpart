from django.db.models.expressions import Exists
import datetime
from django.core import serializers
from users.models import CustomUser, Wishlist
from main.models import HomePage_main_banners
from shop.models import (
    Brand,
    Model,
    Category,
    ManfactureDate,
    EngineCapacity,
    Product,
    HomePage_adds,
    HomePage_banners,
    ReviewProduct,
    Blog_tags,
    Blog,
    ContactUs
)
from orders.models import ShippingCosts, Order, OrderItem, PromoCodes
from .serializers import (
    CustomUserSerializer,
    ModelOfCarSerializer,
    BrandSerializer,
    EngineCapacitySerializer,
    ManfactureDateSerializer,
    CategorySerializer,
    ProductSerializer,
    HomePage_addsSerializer,
    HomePage_bannersSerializer,
    Blog_tagsSerializer,
    BlogSerializer,
    ReviewProductSerializer,
    ShippingCostsSerializer,
    OrderSerializer,
    OrderItemSerializer,
    OrderItemViewSerializer,
    ProductSearchSerializer,
    ContactUsSerializer,
    RatingSerializer,
    UserRatingSerializer,
    OrderUpdateSerializer,
    WishlistSerializer,
    PromoCodesSerializer,
    OrderDetailsSerializer,
)

from star_ratings.models import Rating, UserRating
from rest_framework.reverse import reverse
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)

# mixins.CreateModelMixin,
# mixins.RetrieveModelMixin,
# mixins.UpdateModelMixin,
# mixins.DestroyModelMixin,
# mixins.ListModelMixin,
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, permissions, mixins, generics
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import status

from django.db.models import Q, fields, query

import django_filters.rest_framework
from rest_framework import filters

from rest_framework.response import Response
from rest_framework.views import APIView

import requests

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from users.tokens import account_activation_token
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework_api_key.permissions import HasAPIKey


from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import BrowsableAPIRenderer

class CustomRenderer(JSONRenderer):        
        def render(self, data, accepted_media_type=None, renderer_context=None):
            response = {
                # 'error': False,
                # 'message': 'Success',
                'data': data,
            }

            return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit or view it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):   
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

@api_view(["POST", "GET"])
@permission_classes([permissions.AllowAny])
@authentication_classes((TokenAuthentication,))
def UserActivationView(request):
    user_id = request.GET.get("user_id")
    timestamp = request.GET.get("timestamp")
    signature = request.GET.get("signature")
    protocol = "https://" if request.is_secure() else "http://"
    web_url = protocol + request.get_host()
    # post_url = "http://127.0.0.1:8000/api/v1/accounts/verify-registration/"
    # post_url = "https://marchpart.com/api/v1/accounts/verify-registration/"
    post_url = web_url + "/api/v1/accounts/verify-registration/"
    # headers = {"Authentication": "Token " + token}
    post_data = {
        "user_id": user_id,
        "timestamp": timestamp,
        "signature": signature,
    }
    result = requests.post(post_url, data=post_data)
    content = result.text
    # print(user_id)
    # print(timestamp)
    # print(signature)
    if result.status_code == 200:
        try:
            user = CustomUser.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        # if user is not None and account_activation_token.check_token(user, token):
        if user is not None:
            # user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("shop:home")
    else:
        return render(request, "account_activation_invalid.html")

    # return Response(content)
    return Response(
        content,
        status=result.status_code,
    )


def UserResetPasswordView(request):
    user_id = request.GET.get("user_id")
    timestamp = request.GET.get("timestamp")
    signature = request.GET.get("signature")
    password = None
    password = request.GET.get("password")
    context = {
        "user_id": user_id,
        "timestamp": timestamp,
        "signature": signature,
    }

    if password is not None:
        protocol = "https://" if request.is_secure() else "http://"
        web_url = protocol + request.get_host()
        # post_url = "http://127.0.0.1:8000/api/v1/accounts/reset-password/"
        # post_url = "https://marchpart.com/api/v1/accounts/reset-password/"
        post_url = web_url + "/api/v1/accounts/reset-password/"
        post_data = {
            "password": password,
            "user_id": user_id,
            "timestamp": timestamp,
            "signature": signature,
        }
        r = requests.post(post_url, data=post_data)
        print(password)
        print(user_id)
        print(timestamp)
        if r.status_code == 200:
            return HttpResponse("password reset successfully 200 ok status")
        else:
            return HttpResponse("password reset FAILED!!")

    return render(request, "restFramework_password_reset_confirm.html", context)


def UserGETResetPasswordView(request):
    user_id = request.GET.get("user_id")
    timestamp = request.GET.get("timestamp")
    signature = request.GET.get("signature")
    password = request.GET.get("password")
    # if password is not None:
    protocol = "https://" if request.is_secure() else "http://"
    web_url = protocol + request.get_host()
    # post_url = "http://127.0.0.1:8000/api/v1/accounts/reset-password/"
    # post_url = "https://marchpart.com/api/v1/accounts/reset-password/"
    post_url = web_url + "/api/v1/accounts/reset-password/"
    post_data = {
        "password": password,
        "user_id": user_id,
        "timestamp": timestamp,
        "signature": signature,
    }
    r = requests.post(post_url, data=post_data)
    print(password)
    print(user_id)
    print(timestamp)
    if r.status_code == 200:
        return render(request, "password_reset_complete.html")
    else:
        return HttpResponse("password reset FAILED!!")
    return HttpResponse("nothing happened")




class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)


class CustomUserViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet, permissions.BasePermission
):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return CustomUser.objects.filter(email=user.email)


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes((TokenAuthentication,))
def customUser_edit_endpoint(request, city, province, country, mobile):
    user = request.user
    custom_user = CustomUser.objects.get(id=user.id)
    if city != "none":
        custom_user.city=city
    if province != "none":
        custom_user.province=province
    if country != "none":
        custom_user.country=country
    if mobile != "none":
        custom_user.mobile=mobile
    # if first_name != "none":
    #     custom_user.first_name=first_name
    custom_user.save()
    return Response({
        'detail': 'data updated'
    })


class WishlistCreate(mixins.CreateModelMixin,  viewsets.GenericViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(get_user=self.request.user)

    def create(self, request, *args, **kwargs):
        if Wishlist.objects.filter(get_user=self.request.user, product=self.request.data['product']).exists():
            return Response({'error': 'you already added this product to wishlist'})
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes((TokenAuthentication, OAuth2Authentication))
def wishlist_delete_rest_endpoint(request, id):
    user = request.user
    if Wishlist.objects.filter(product_id=id).exists(): 
        # wishlist = Wishlist.objects.get(product_id=id)    
        # if user == wishlist.get_user:
        Wishlist.objects.filter(product_id=id, get_user=user).delete()
        return Response({'detail': 'deleted'})
        # else:
        #     return HttpResponse('User Not Owner')
    else:
        return Response(
            {'error': 'Item Not Found'}
        )


class WishlistViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet, permissions.BasePermission
):

    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Wishlist.objects.filter(get_user=user)




class ModelOfCarViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Model.objects.all()
    serializer_class = ModelOfCarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["brand", "name", "name_arabic", "slug", "id"]
    # permission_classes = [permissions.IsAuthenticated]



class ModelOfCarViewSetNoPagination(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Model.objects.all()
    serializer_class = ModelOfCarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["brand", "name", "name_arabic", "slug", "id"]
    pagination_class = None
    # permission_classes = [permissions.IsAuthenticated]


class BrandViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Brand.objects.all().order_by("name")
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "name_arabic", "slug", "id"]
    # permission_classes = [permissions.IsAuthenticated]

class BrandViewSetALL(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Brand.objects.all().order_by("name")
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "name_arabic", "slug", "id"]
    pagination_class = LargeResultsSetPagination



class BrandViewSetALLِArabic(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Brand.objects.all().order_by("name_arabic")
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "name_arabic", "slug", "id"]
    pagination_class = LargeResultsSetPagination


class EngineCapacityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = EngineCapacity.objects.all().order_by("eng_capacity")
    serializer_class = EngineCapacitySerializer
    pagination_class = None
    # permission_classes = [permissions.IsAuthenticated]


class ManfactureDateViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = ManfactureDate.objects.all().order_by("manfacture_year")
    serializer_class = ManfactureDateSerializer
    pagination_class = None
    # permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "name_arabic", "slug", "id"]
    # permission_classes = [permissions.IsAuthenticated]


# class ProductViewSet(mixins.ListModelMixin, APIView):
class ProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Product.objects.all().order_by("name")
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "id",
        "name",
        "name_arabic",
        "slug",
        "model",
        "engine_capacity",
        "manfacture_date",
        "seller_recommendation",
        "hidden",
    ]
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        reduced_prices = str(self.request.query_params.get("reduced")).lower()
        seller_recommendation = str(self.request.query_params.get("recommend")).lower()
        #    if only_missing in ['true', '1']:
        #        return qs.filter(returned__isnull=True)
        if reduced_prices in ["true", "1"]:
            return qs.filter(sale_price__isnull=False, hidden=False)[:12]
        if seller_recommendation in ["true", "1"]:
            return qs.filter(seller_recommendation=False, hidden=False)[:12]
        return qs

 

class ReviewProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = ReviewProduct.objects.all().order_by("pub_date")
    serializer_class = ReviewProductSerializer
    # permission_classes = [permissions.IsAuthenticated]


class HomePage_addsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = HomePage_banners.objects.all()
    serializer_class = HomePage_addsSerializer
    # permission_classes = [permissions.IsAuthenticated]


class HomePage_bannersViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = HomePage_main_banners.objects.all()
    serializer_class = HomePage_bannersSerializer
    # permission_classes = [permissions.IsAuthenticated]


class Blog_tagsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Blog_tags.objects.all()
    serializer_class = Blog_tagsSerializer
    permission_classes = [permissions.AllowAny,]

class UserRatingViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserRating.objects.all()
    serializer_class = UserRatingSerializer
    permission_classes = [permissions.AllowAny,]

class UserRatingCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UserRating.objects.all()
    serializer_class = UserRatingSerializer
    # permission_classes = [permissions.IsAuthenticated,]
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class RatingViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.AllowAny,]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "object_id",
    ]

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes((OAuth2Authentication, TokenAuthentication))
def customRating(request, product_id, score):
    user = request.user
    r = Rating.objects.get(object_id=product_id)
    filterRate = UserRating.objects.filter(rating=r, user=user)
    if filterRate:
        return Response({'detail': 'user already rated this product'})
    else:
        ur = UserRating.objects.create(rating=r, user=user, score=score)
        return Response({
            "status": "producted rated",
            "detail": str(ur)
        })



class BlogViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny,]

class LastThreeBlogsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Blog.objects.all().order_by('-created_at')[0:3]
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny,]

class ContactUSViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [permissions.AllowAny,]

# ##Create Order:

# class OrderCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated,]

class OrderCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated,]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderItemsCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated,]



class OrderUPdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()    
    serializer_class = OrderUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, HasAPIKey]

    # def get_serializer(self, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return super(OrderSerializer, self).get_serializer(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('fees', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            order_items = OrderItem.objects.filter(order__id = serializer.data['id'])
            current_site = get_current_site(request)
            subject = "Invoice"
            messageTest = render_to_string(
                "orders/order/order-email.html",
                {
                    "domain": current_site.domain,
                    'fees' : serializer.data['fees'],
                    'first_name' : serializer.data['first_name'],
                    'last_name' : serializer.data['last_name'],
                    'email' : serializer.data['email'],
                    'user' : serializer.data['user'],
                    'city' : serializer.data['city'],
                    'address' : serializer.data['address'],
                    'phone1' : serializer.data['phone1'],
                    'phone2' : serializer.data['phone2'],
                    'invoice' : serializer.data['code'],
                    'order_items' : order_items,
                },
            )
            to_emails = [
                (serializer.data['email']),
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
            return Response(serializer.data)
        else:
            return HttpResponse('nothing updated')


########################################################################################################
####################################  Customized SERIALIZERS ###########################################
########################################################################################################


class SearchAPI(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "name_arabic","id", "=hidden", "category__name", "model__name", "model__brand__name"]

class SearchByModelAPI(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        queryset = Product.objects.all()
        model = self.kwargs.get('model', None)
        manfacture_date = self.kwargs.get('manfacture_date', None)
        engine_capacity = self.kwargs.get('engine_capacity', None)

        if manfacture_date != 'none' and engine_capacity == 'none':  
            queryset = queryset.filter(
                Q(model__name__iexact=model,
                engine_capacity__isnull=True,
                manfacture_date__manfacture_year=manfacture_date,
                hidden=False)|Q(model__name__iexact=model,
                    manfacture_date__manfacture_year=manfacture_date,
                    hidden=False
                ) |
                Q(model__name_arabic__iexact=model,
                engine_capacity__isnull=True,
                manfacture_date__manfacture_year=manfacture_date,
                hidden=False)|Q(model__name_arabic__iexact=model,
                    manfacture_date__manfacture_year=manfacture_date,
                    hidden=False
                )|Q(model__name__iexact=model,
                hidden=False) |
                Q(model__name_arabic__iexact=model,
                hidden=False)
                ).distinct('name').order_by("name")

        if engine_capacity != "none" and manfacture_date != 'none':  
            queryset = queryset.filter(
                Q(model__name__iexact=model,
                engine_capacity__eng_capacity=engine_capacity,
                manfacture_date__manfacture_year=manfacture_date,
                hidden=False) |
                Q(model__name_arabic__iexact=model,
                engine_capacity__eng_capacity=engine_capacity,
                manfacture_date__manfacture_year=manfacture_date,
                hidden=False) |
                Q(model__name__iexact=model,
                manfacture_date__manfacture_year=manfacture_date,
                hidden=False) |
                Q(model__name_arabic__iexact=model,
                manfacture_date__manfacture_year=manfacture_date,
                hidden=False)|Q(model__name__iexact=model,
                hidden=False) |
                Q(model__name_arabic__iexact=model,
                hidden=False)
                ).distinct('name').order_by("name")

        if engine_capacity == "none" and manfacture_date == 'none':  
            queryset = queryset.filter(
                Q(model__name__iexact=model,
                hidden=False) |
                Q(model__name_arabic__iexact=model,
                hidden=False)
                ).order_by("name")

        if engine_capacity != "none" and manfacture_date == 'none':  
            queryset = queryset.filter(
                Q(model__name__iexact=model,
                engine_capacity__eng_capacity=engine_capacity,
                hidden=False) |
                Q(model__name_arabic__iexact=model,
                engine_capacity__eng_capacity=engine_capacity,
                hidden=False)|Q(model__name__iexact=model,
                hidden=False) |
                Q(model__name_arabic__iexact=model,
                hidden=False)
                ).distinct('name').order_by("name")
        return queryset
        


class FilterProductsByCategory(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["category__name"]


# class BooleansFilterSet(django_filters.FilterSet):
#        reduced = django_filters.BooleanFilter(field_name='sale_price', lookup_expr='isnull')

#    class Meta:
#        model = models.Borrowed
#        fields = ['what', 'to_who', 'missing']


class ProductQueries(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    # #i should use this also with ModelViewSet to limit the allowed http methods:
    # http_method_names = ['get', 'options', 'head']

    def get_queryset(self):
        queryset = Product.objects.all().filter(hidden=False)
        new_arrivals = self.request.query_params.get("new", None)
        reduced_prices = self.request.query_params.get("reduced", None)
        seller_recommendation = self.request.query_params.get("recommend", None)
        # if reduced_prices is not None:
        if reduced_prices is not None:
            if reduced_prices == "true":
                queryset = queryset.filter(sale_price__isnull=False).order_by("?")[:12]
            elif reduced_prices == "false":
                queryset = queryset.filter(sale_price__isnull=True).order_by("?")[:4]
        if seller_recommendation is not None:
            if seller_recommendation == "true":
                queryset = queryset.filter(seller_recommendation=True).order_by("?")[
                    :12
                ]
        if new_arrivals is not None:
            if new_arrivals == "true":
                queryset = queryset.order_by("-created_at").order_by("?")[:12]
        return queryset

    ########################################################################################################
    ####################################  ORDERS SERIALIZERS ###############################################
    ########################################################################################################


@api_view(["GET"])
def PromCodeViewSet(request, promoCode):
    date_now = datetime.datetime.now()
    try:
        checkPromo =  PromoCodes.objects.get(
            promo_code=promoCode,
            valid_from__lte=date_now, 
            valid_to__gte=date_now
            )
        discount = checkPromo.discount_ratio
        return Response(
            {
                'detail': 'promocode available',
                'discount': str(discount)
            }
        )
    except:
        return Response({'detail': 'not valid'})


 

class ShippingCostsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ShippingCosts.objects.all()
    serializer_class = ShippingCostsSerializer
    pagination_class = LargeResultsSetPagination
    # renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    # @action(detail=True)
    # def count(self, request):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     count = queryset.count()
    #     content = {
    #         'count': count,
    #         'result': queryset,
    #         }
    #     return Response(content)
    # permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)






class OrderItemViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemViewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        get_order_id = self.request.query_params.get('order-id')
        order = Order.objects.get(id=get_order_id)
        return OrderItem.objects.filter(order__user=user, order_id=order.id)


