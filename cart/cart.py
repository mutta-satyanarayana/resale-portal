from django.conf import settings
from product.models import Product
from decimal import Decimal

class Cart(object):
    # --> Create Cart & Add Products into Cart & update Quantity
    def __init__(self, request):
        """
        Intialize the Cart
        """
        self.session  = request.session
        cart = request.session.get(settings.CART_SESSION_ID)
        if not cart:
            """ Save Empty Session in Cart """
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity = 1, update_quantity = False):
        " Add Product to Cart or Update quntity in cart"
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price': str(product.price)}
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets save
        self.session.modified = True

    # ---> Remove Cart
    def remove(self, product):
        # remove product from cart
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    #--> Clear Cart
    def __iter__(self):
        """
        Interate over the items in the cart and get the products from the database
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # --> Total Price in Cart
    def __len__(self):
        # return count of products
        return sum(item['quantity'] for item in self.cart.values())

    #--> get total price from cart
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    #--> Clear products
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
