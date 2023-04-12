from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # self.session.set_expiry(5)

    def add(self, product, quantity=1, update_quantity=False, price=None):
        product_id = str(product.id)
        if product_id not in self.cart:
            if product.sale_price == None or product.sale_price == 0:
                self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
            elif product.sale_price != None and product.sale_price != 0:
                self.cart[product_id] = {
                    "quantity": 0,
                    "price": str(product.sale_price),
                }
            else:
                self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def update(self, product, quantity=1, price=None):
        product_id = str(product.id)       
        if product.sale_price == None or product.sale_price == 0:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        elif product.sale_price != None and product.sale_price != 0:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.sale_price),
            }       
        self.cart[product_id]["quantity"] = quantity
        self.save()

    # Original cart before updates of price:
    # def add(self, product, quantity=1, update_quantity=False):
    #     product_id = str(product.id)
    #     if product_id not in self.cart:
    #         if product.sale_price == None:
    #             self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
    #         if product.sale_price != None:
    #             self.cart[product_id] = {'quantity': 0, 'price': str(product.sale_price)}

    #     if update_quantity:
    #         self.cart[product_id]['quantity'] = quantity
    #     else:
    #         self.cart[product_id]['quantity'] += quantity
    #     self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clean(self):
        self.cart.clear()
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]["product"] = product

        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def get_items(self):
        return (item["quantity"] for item in self.cart.values())
        

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
