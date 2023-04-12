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
    ContactUs,
    
)
from orders.models import ShippingCosts, Order, OrderItem, PromoCodes
from rest_framework import serializers

from star_ratings.models import Rating, UserRating




class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = [
        #     'id', 'first_name', 'last_name', 'photo', 'password',
        #     'username', 'country', 'agreement', 'email',
        # ]
        fields = "__all__"


# class CustomUserCreateSerializer(BaseUserRegistrationSerializer):
#     class Meta(BaseUserRegistrationSerializer.Meta):
#         model = CustomUser
#         # fields = [
#         #     'id', 'first_name', 'last_name', 'photo', 'password',
#         #     'username', 'country', 'agreement', 'email',
#         # ]
#         fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ModelOfCarSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name')
    class Meta:
        model = Model
        fields = "__all__"


class EngineCapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineCapacity
        fields = "__all__"


class ManfactureDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManfactureDate
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

#     return self.fields[key]
# KeyError: 'results'
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    manfacture_date = ManfactureDateSerializer(read_only=True, many=True)
    model = ModelOfCarSerializer(read_only=True, many=True)
    # url_arabic = serializers.URLField("https://marchpart.com/shop/arabiclanguage/product/arabiclanguage/<id>/<slug>")
    # url_english = serializers.URLField()
    # brand_name = serializers.CharField(source='model.brand.name')
    class Meta:
        model = Product
        fields = "__all__"
    
    def to_representation(self, instance):
        ret = super(ProductSerializer, self).to_representation(instance)
        # check the request is list view or detail view
        # is_list_view = isinstance(self.instance, list)
        extra_ret = {
            'url_english': 'https://marchpart.com/shop/englishlanguage/product/englishlanguage/' + str(instance.id) + '/' + str(instance.slug),
            'url_arabic': 'https://marchpart.com/shop/arabiclanguage/product/arabiclanguage/'  + str(instance.id) + '/' + str(instance.slug)
            } 
            # if is_list_view else {'key': 'single value'}
        ret.update(extra_ret)
        return ret

class ReviewProductSerializer(serializers.ModelSerializer):
    rate_score = serializers.CharField(source="rate.score")  # this for foriegnKeys

    class Meta:
        model = ReviewProduct
        # fields = ['rate_score',] ### '__all__' ... Note: can't use __all__  so i ve to add the fields names
        fields = "__all__"


class HomePage_addsSerializer(serializers.ModelSerializer):
    slide_image = serializers.ImageField(source='banner_image')
    class Meta:
        model = HomePage_banners
        fields = "__all__"


class HomePage_bannersSerializer(serializers.ModelSerializer):
    slide_image = serializers.ImageField(source='banner_image')
    slide_title = serializers.CharField(source='banner_title')
    class Meta:
        model = HomePage_main_banners
        fields = "__all__"


class Blog_tagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog_tags
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
    def to_representation(self, instance):
        ret = super(BlogSerializer, self).to_representation(instance)
        # check the request is list view or detail view
        # is_list_view = isinstance(self.instance, list)
        extra_ret = {
            'url_english': 'https://marchpart.com/shop/englishlanguage/englishlanguage/blog-details/' + str(instance.slug),
            'url_arabic': 'https://marchpart.com/shop/arabiclanguage/arabiclanguage/blog-details/' + str(instance.slug),
            } 
            # if is_list_view else {'key': 'single value'}
        ret.update(extra_ret)
        return ret

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"



class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"

class UserRatingSerializer(serializers.ModelSerializer):
    # product_name = serializers.CharField(source='rating.content_object.name')
    # product_id = serializers.CharField(source='rating.content_object.id')
    class Meta:
        model = UserRating
        fields = "__all__"
    # def validate(self, attrs):
    #     user = attrs.get('user', self.object.user)
    #     rating = attrs.get('rating', self.object.rating)

    #     try:
    #         obj = Model.objects.get(user=user, rating=rating)
    #     except DoesNotExist:
    #         return attrs
    #     if self.object and obj.id == self.object.id:
    #         return attrs
    #     else:
    #         raise serializers.ValidationError('user with rating already exists')
###############################################################################################################
######################################## Customized Serializers ###############################################
###############################################################################################################
class ProductSearchSerializer(serializers.ModelSerializer):
    # manfacture_date = ManfactureDateSerializer(read_only=True, many=True)
    # engine_capacity = serializers.CharField(source='engine_capacity.eng_capacity')
    class Meta:
        model = Product
        fields = "__all__"


######################################################################################################
######################################## ORDERS MODELS ###############################################
######################################################################################################


class PromoCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCodes
        fields = "__all__"

class ShippingCostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCosts
        fields = "__all__"


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # fields = "__all__"
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'country', 'phone1', 'phone2', 'id', 'code', 'promo_code'] 

class OrderDetailsSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)
    class Meta:
        model = Order
        fields = "__all__"



class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source="order.id")  # this for foriegnKeys
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemViewSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source="order.id")  # this for foriegnKeys
    product_name_arabic = serializers.CharField(source="product.name_arabic")
    product_name = serializers.CharField(source="product.name")
    image = serializers.ImageField(source="product.image")

    class Meta:
        model = OrderItem
        fields = '__all__'
        # fields = [
        #     "order_id",
        # ]


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


class WishlistSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source="product", read_only=True)
    # product_name = serializers.CharField(source='product.name', required=False)
    # product_name_arabic = serializers.CharField(source='product.name_arabic', required=False)
    # product_price = serializers.CharField(source='product.price', required=False)
    # product_sale_price = serializers.CharField(source='product.sale_price', required=False)
    # product_available = serializers.CharField(source='product.available', required=False)
    class Meta:
        model = Wishlist
        fields = "__all__"
        # depth = 1
    # def create(self, validated_data): ## To Prevent Dublicate
    #     products_data = validated_data.pop('product')
    #     wishlist = Wishlist.objects.create(**validated_data)
    #     for product_data in products_data:
    #         tag = Tag.objects.get_or_create(**tag_data)[0]
    #         wishlist.tag.add(tag)
    #     return wishlist

