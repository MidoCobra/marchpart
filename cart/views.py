from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product, Category
from .cart import Cart
from .forms import CartAddProductForm

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse, response
import json
from decimal import Decimal

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])

    return redirect('cart:cart_detail')


@csrf_exempt
def AjaxAddCart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # product_id = product.id
#     form = CartAddProductForm(request.POST)
    # username = request.user    

    #from ajax create post:
    # if username is None:
    #     response_data={}
    #     response_data['no_user'] = 'no_user'
    #     return JsonResponse(response_data)

    if request.method == 'POST':
        update_cart = request.POST.get('update')
        quantity_cart = request.POST.get('quantity')
        

        response_data = {}

        cart.add(product=product, quantity= int(quantity_cart), update_quantity= update_cart)
        cart.save()   
        return JsonResponse(response_data)
    


@require_POST
def cart_add_arabic(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])

    return redirect('cart:cart_detail_arabic')

def cart_remove(request, product_id=None):
    cart = Cart(request)
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
    else:
        products = Product.objects.all()
        cart.clean()       
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()
    
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart, 'categories':categories})

def cart_remove_arabic(request, product_id=None):
    cart = Cart(request)
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
    else:
        products = Product.objects.all()
        cart.clean()       
    return redirect('cart:cart_detail_arabic')


def cart_detail_arabic(request):
    cart = Cart(request)
    categories = Category.objects.all()
    
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail_arabic.html', {'cart': cart, 'categories':categories})
