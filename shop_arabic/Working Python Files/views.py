from django.shortcuts import render, get_object_or_404
from main.models import HomePage_main_banners_WEBSITE
from shop.models import (
    Category,
    Product,
    Brand,
    Model,
    EngineCapacity,
    ManfactureDate,
    ReviewProduct,
    HomePage_adds,
    HomePage_banners,
    Blog,
    Blog_tags,
    ContactUs,
)
from shop.forms import ReviewProductForm, ContactUsForm
from orders.models import OrderItem, Order
from django.contrib.contenttypes.models import ContentType
from star_ratings.models import Rating, UserRating, RatingManager, UserRatingManager
from cart.forms import CartAddProductForm
from orders.models import Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# For Search bar:
from django.db.models import Q
import datetime
from datetime import date, timedelta
from django.contrib import messages
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
    response,
)

# to restrict access to  functions:
from django.contrib.auth.decorators import login_required

# to restrict access to  base genric classes:
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Count, F, Sum

from cart.cart import Cart
from cart.forms import CartAddProductForm


# HOME PAGE ##:
def Home_arabic(request, category_slug=None):
    category = None
    form = CartAddProductForm(request.POST)
    categories = Category.objects.all()
    products = Product.objects.all().exclude(hidden=True)[:9]
    # products = Product.objects.all().filter(rate_product__isnull=False).order_by('rate_product__average')[:9]
    best_seller = (
        Product.objects.all()
        .exclude(hidden=True)
        .exclude(order_items__isnull=True)
        .annotate(x=Sum("order_items__quantity"))
        .order_by("-x")
        .reverse()[:6]
    )
    new_arrivals = (
        Product.objects.all().order_by("-created_at").exclude(hidden=True)[:4]
    )
    new_arrivals2 = (
        Product.objects.all().order_by("-created_at").exclude(hidden=True)[4:8]
    )
    reduced_prices = (
        Product.objects.filter(sale_price__isnull=False)
        .order_by("?")
        .exclude(hidden=True)[:4]
    )
    reduced_prices2 = (
        Product.objects.filter(sale_price__isnull=False)
        .order_by("?")
        .exclude(hidden=True)[:4]
    )
    seller_recommendation = (
        Product.objects.filter(seller_recommendation=True)
        .order_by("?")
        .exclude(hidden=True)[:4]
    )
    seller_recommendation2 = (
        Product.objects.filter(seller_recommendation=True)
        .order_by("?")
        .exclude(hidden=True)[:4]
    )
    # products = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, hidden=False)

    page = request.GET.get("page", 1)

    paginator = Paginator(products, 15)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    #####################
    get_brand = None
    modelSearch = None
    response_data = {}
    if request.is_ajax and request.method == "POST":
        get_brand = request.POST.get("search_brand_arabic", None)
        modelSearch = Model.objects.filter(brand__name_arabic__exact=get_brand)
        all_name = []
        all_id = []
        for m in modelSearch:
            all_id.append(m.id)
            all_name.append(m.name_arabic)
        data = {
            "modelQuerySet": all_name
            # 'modelQueySet': serializers.serialize("json", all_name)
        }
        return JsonResponse(data)

    brand = Brand.objects.all()

    ##>>>>  For Search box <<<<##
    brands = Brand.objects.all().order_by("name_arabic")
    models = Model.objects.all()
    enginecc = EngineCapacity.objects.all().order_by("eng_capacity")
    manYear = ManfactureDate.objects.all().order_by("manfacture_year")
    partTypes = Category.objects.all()

    blogs = Blog.objects.all()[:3]
    homeAdds = HomePage_main_banners_WEBSITE.objects.all()
    homeBanners = HomePage_banners.objects.all()

    context = {
        "form": form,
        "category": category,
        "categories": categories,
        "products": products,
        "products_paginator": products_paginator,
        "brand": brand,
        "brands": brands,
        "models": models,
        "enginecc": enginecc,
        "manYear": manYear,
        "partTypes": partTypes,
        "best_seller": best_seller,
        "new_arrivals": new_arrivals,
        "new_arrivals2": new_arrivals2,
        "reduced_prices": reduced_prices,
        "reduced_prices2": reduced_prices2,
        "seller_recommendation": seller_recommendation,
        "seller_recommendation2": seller_recommendation2,
        "modelSearch": modelSearch,
        "get_brand": get_brand,
        "homeAdds": homeAdds,
        "homeBanners": homeBanners,
        "blogs": blogs,
        # 'results': results,
    }
    u = request.user
    # if u.is_authenticated:
    return render(request, "shop_arabic/product_arabic/home_arabic.html", context)
    # elif u.is_anonymous:
    #     return render(request, 'shop/product/comingSoon.html')


def AllBrandsCategoryProducts_arabic(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, hidden=False)

    page = request.GET.get("page", 1)
    paginator = Paginator(products, 40)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context = {
        "category": category,
        "products": products,
        "products_paginator": products_paginator,
    }
    return render(request, "shop_arabic/category_arabic.html", context)


def product_detail_arabic(request, id, slug):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id, slug=slug)
    products = Product.objects.all().exclude(id=product.id)[:4]
    categories = Category.objects.all()
    category = product.category
    # similar_products = Product.objects.filter(
    #     category=category, model=product.model).exclude(id=product.id)[:7]
    form = CartAddProductForm()
    reviews = ReviewProduct.objects.filter(product=product).order_by("-pub_date")[:25]
    user = request.user
    user_review = ReviewProduct.objects.filter(
        user_name=user.username, product=product.id
    )
    # i used this to get the model as instance for content_type in star ratings, and imported ContentType from django models
    content_type_instance = ContentType.objects.get_for_model(Product)
    # object_id = Rating.objects.get(object_id=tour.id, content_type=content_type_instance)
    # object_id = get_object_or_404(Rating,object_id=tour.id, content_type=content_type_instance)
    score = UserRating.objects.filter(reviewproduct__in=reviews).count()
    score1 = UserRating.objects.filter(reviewproduct__in=reviews, score=1).count()
    score2 = UserRating.objects.filter(reviewproduct__in=reviews, score=2).count()
    score3 = UserRating.objects.filter(reviewproduct__in=reviews, score=3).count()
    score4 = UserRating.objects.filter(reviewproduct__in=reviews, score=4).count()
    score5 = UserRating.objects.filter(reviewproduct__in=reviews, score=5).count()
    try:  # i used this to avoid the zerodivisonerror if score = 0
        score1Ratio = int((score1 * 100) / score)
        score2Ratio = int((score2 * 100) / score)
        score3Ratio = int((score3 * 100) / score)
        score4Ratio = int((score4 * 100) / score)
        score5Ratio = int((score5 * 100) / score)
    except ZeroDivisionError:
        score1Ratio = 0
        score2Ratio = 0
        score3Ratio = 0
        score4Ratio = 0
        score5Ratio = 0
    try:
        count_reviews = ReviewProduct.objects.filter(product=product.name).count()
    except:
        count_reviews = 0
    form_review = ReviewProductForm(request.POST)

    for x in cart:
        print(x["product"])
    my_iter_list = iter(cart)
    # print(my_iter_list)
    # for x in request.session.items():
    #     print(x)
    context = {
        "product": product,
        "form": form,
        # 'similar_products': similar_products,
        "categories": categories,
        "form_review": form_review,
        "categories": categories,
        "count_reviews": count_reviews,
        "reviews": reviews,
        "user_review": user_review,
        "category": category,
    }
    return render(request, "shop_arabic/product_arabic/detail_arabic.html", context)


@login_required(login_url="login")
@csrf_exempt
def AjaxAddReviewProduct(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_id = product.id
    # username = request.user.id
    username = request.user
    # avatar = request.user.photo.url
    rate = UserRating.objects.filter(user=username)
    # i used this to get the model as instance for content_type in star ratings, and imported ContentType from django models
    content_type_instance = ContentType.objects.get_for_model(Product)
    object_id = Rating.objects.get(
        object_id=product_id, content_type=content_type_instance
    )

    # from ajax create post:
    if username is None:
        response_data = {}
        response_data["no_user"] = "no_user"
        return JsonResponse(response_data)

    if request.method == "POST":
        post_text = request.POST.get("the_post")
        # post_rate = request.POST.get('the_rate')
        response_data = {}
        post_fake = ReviewProduct(user_name=username, product=product.name)
        if ReviewProduct.objects.filter(
            product=post_fake.product, user_name=post_fake.user_name
        ).exists():
            return JsonResponse(response_data)
        else:
            try:
                rate_result = rate.get(rating=object_id)
                post = ReviewProduct(
                    comment=post_text,
                    rate=rate_result,
                    user_name=username,
                    product=product.name,
                    pub_date=datetime.datetime.now(),
                )
                # I Think i have to save the post here! gonna check that later!
            except (KeyError, UserRating.DoesNotExist):
                response_data["no_rate"] = "no_rate"
                return JsonResponse(response_data)

            else:
                rate_result = rate.get(rating=object_id)
                post = ReviewProduct(
                    comment=post_text,
                    rate=rate_result,
                    user_name=username.username,
                    product=product.name,
                    pub_date=datetime.datetime.now(),
                )
                post.save()
                response_data["comment"] = post.comment
                response_data["product"] = post.product
                response_data["pub_date"] = post.pub_date
                response_data["user_name"] = post.user_name
                return JsonResponse(response_data)
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json",
        )


def search_arabic(request):
    brands = Brand.objects.all()
    models = Model.objects.all()
    enginecc = EngineCapacity.objects.all()
    manYear = ManfactureDate.objects.all()
    partTypes = Category.objects.all()
    results = None
    results2 = None
    results3 = None
    if request.method == "GET":
        # brandSearch = request.GET.get('brandSearch')
        modelSearch = request.GET.get("modelSearch")
        engineSearch = request.GET.get("engineSearch")
        manfactureSearch = request.GET.get("manfactureSearch")
        partTypeSearch = request.GET.get("partTypeSearch")
        productSearch = request.GET.get("productSearch")
        # if not engineSearch or not manfactureSearch:
        #     results = Product.objects.filter(
        #         model__name__iexact=modelSearch,
        #         hidden=False,
        #     )
        # else:
        if engineSearch:
            try:
                results = Product.objects.filter(
                    model__name_arabic__contains=modelSearch,
                    engine_capacity__eng_capacity=engineSearch,
                    manfacture_date__manfacture_year=manfactureSearch,
                    hidden=False
                    # , name__icontains=productSearch
                    #  category__name=partTypeSearch,
                )
            except:
                results = Product.objects.filter(
                    model__name_arabic__contains=modelSearch,
                    engine_capacity__eng_capacity=engineSearch,
                    hidden=False
                    # , name__icontains=productSearch
                    #  category__name=partTypeSearch,
                )
        else:
            results = Product.objects.filter(engine_capacity__eng_capacity=0)
        # query = Q(
        #     manfacture_date=manfactureSearch,
        #     engine_capacity__isnull=True,
        #     model__name_arabic__iexact=modelSearch,
        # )
        # results2 = Product.objects.filter(query)

        if manfactureSearch:
            results2 = Product.objects.filter(
                model__name_arabic__contains=modelSearch,
                engine_capacity__isnull=True,
                manfacture_date__manfacture_year=manfactureSearch,
                hidden=False,
            )
        else:
            results2 = Product.objects.filter(engine_capacity__eng_capacity=0)

        results3 = Product.objects.filter(
            model__name_arabic__iexact=modelSearch,
            # engine_capacity__isnull=True,
            # manfacture_date__isnull=True,
            hidden=False,
        )
        page = request.GET.get("page", 1)
        paginator = Paginator(results3, 60)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        # try:
        #     if results == None:
        #         results = 0
        #     if results2 == None:
        #         results2 = 0
        #     if results3 == None:
        #         results3 = 0
        counter = (
            int(results.count()) + int(results2.count()) + int(results3.count())
        )
        # except:
        #     counter = 6

        context = {
            "brands": brands,
            "models": models,
            "enginecc": enginecc,
            "manYear": manYear,
            "partTypes": partTypes,
            "results": results,
            "results2": results2,
            "results3": products_paginator,
            "counter": counter,
            "manfactureSearch": manfactureSearch,
            "products_paginator": products_paginator,
        }
        return render(request, "searchResults_arabic.html", context)
    else:
        return render(request, "searchResults_arabic.html")


def NavbarSearch_arabic(request):
    # results=None
    productSearchAllTypes = request.GET.get("productSearchAllTypes")
    # model__name for ban searching for another categories
    results = Product.objects.filter(Q(
        name_arabic__icontains=productSearchAllTypes, 
        hidden=False
    )|Q(
        name__icontains=productSearchAllTypes, 
        hidden=False
    )|Q(
        search_tags__icontains= productSearchAllTypes,
        hidden=False
    )
    )

    page = request.GET.get("page", 1)
    paginator = Paginator(results, 60)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)  
    try:
        productSearchAllTypes = int(productSearchAllTypes)
        results2 = Product.objects.filter(id=productSearchAllTypes)
    except:
        results2 = None
    counter=None
    if results and results2:
        counter= int(results.count() + results2.count())
    elif results:
        counter = results.count()
    elif results2:
        counter = results2.count()
    context = {
        "results": results,
        "results2": results2,
        "counter": counter,
        "products_paginator": products_paginator,
    }
    return render(request, "searchResults_arabic_nav.html", context)


def ModelsView_arabic(request, brandSlug):
    models = Model.objects.filter(brand__slug=brandSlug).order_by("name_arabic")
    brand = get_object_or_404(Brand, slug=brandSlug)
    context = {
        "models": models,
        "brand": brand,
    }
    return render(request, "models_arabic.html", context)


def ModelCategories_arabic(request, modelSlug):
    model = get_object_or_404(Model, slug=modelSlug)

    category = (
        Category.objects.all()
        .exclude(~Q(products__model__slug=modelSlug))
        .distinct("name")
    )  # this means not equal
    # category = Category.objects.all().exclude(products__model = None)
    categoryForAllModels = Category.objects.filter(products__isnull=True).distinct(
        "name"
    )

    # category = (
    #     Category.objects.all()
    #     .exclude(~Q(products__model__slug=modelSlug))
    # )  # this means not equal
    # # category = Category.objects.all().exclude(products__model = None)
    # categoryForAllModels = Category.objects.filter(products__isnull=True)

    context = {
        "model": model,
        "category": category,
        "categoryForAllModels": categoryForAllModels,
        "model_slug": modelSlug,
    }
    return render(request, "model-categories_arabic.html", context)


def ModelCategoryProducts_arabic(
    request, modelSlug, categorySlug, productsForAllModels
):

    categories = (
        Category.objects.order_by("name_arabic")
        .distinct("name_arabic")
        .exclude(~Q(products__model__slug=modelSlug))
    )  # this means not equal
    categoryForAllModels = (
        Category.objects.filter(products__model=None)
        .order_by("name_arabic")
        .distinct("name_arabic")
    )
    # categories = (
    #     Category.objects.order_by("name_arabic")
    #     .exclude(~Q(products__model__slug=modelSlug))
    # )  # this means not equal
    # categoryForAllModels = (
    #     Category.objects.filter(products__model=None)
    #     .order_by("name_arabic")
    # )
    # categories = Category.objects.order_by("name_arabic").exclude(
    #     ~Q(products__model__slug=modelSlug)
    # )  # this means not equal
    # categoryForAllModels = Category.objects.filter(products__model=None).order_by(
    #     "name_arabic"
    # )

    products = None
    if productsForAllModels == 1:
        products = Product.objects.filter(
            model=None, category__slug=categorySlug, hidden=False
        )
    else:
        products = Product.objects.filter(
            model__slug=modelSlug, category__slug=categorySlug, hidden=False
        )

    modelname = Model.objects.get(slug=modelSlug)
    categoryname = Category.objects.get(slug=categorySlug)

    page = request.GET.get("page", 1)
    paginator = Paginator(products, 15)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context = {
        "products_paginator": products_paginator,
        "categories": categories,
        "categoryForAllModels": categoryForAllModels,
        "model_slug": modelSlug,
        "modelname": modelname,
        "categoryname": categoryname,
        "productsForAllModels": productsForAllModels,
    }

    return render(request, "model-category-products_arabic.html", context)


def BlogByTags_arabic(request, blogTag_slug):
    blogsTag = get_object_or_404(Blog_tags, slug=blogTag_slug)
    blogs = Blog.objects.filter(tag=blogsTag)
    context = {
        "blogsTag": blogsTag,
        "blogs": blogs,
    }

    return render(request, "blogsByTag_arabic.html", context)


def BlogDetails_arabic(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    context = {"blog": blog}

    return render(request, "blogDetails_arabic.html", context)


def ContactViewArabic(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            if request.recaptcha_is_valid:
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                enquiry = form.cleaned_data['enquiry']
                ContactUs.objects.create(name=name, email=email, enquiry=enquiry)
                messages.success(request, 'تم إرسال الطلب بنجاح')

            

    form = ContactUsForm(request.POST or None, request.FILES or None)
    context = {
        'form': form
    }
    return render(request, "contact_arabic.html", context)

def AboutUsArabic(request):
    return render(request, "about-us-arabic.html")