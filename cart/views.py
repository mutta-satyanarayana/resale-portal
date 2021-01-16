from django.shortcuts import render,get_object_or_404, redirect
from .forms import CartAddProductForm
from product.models import Product
from .cart import Cart
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product = product, quantity = cd['quantity'], update_quantity = cd['update'])
    return redirect('cart:cart_detail')


@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id= product_id)
    #print('\n\n',product)
    #print('\n\n',cart)
    cart.remove(product)
    #print('\n\n',cart)
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request):
    cart = Cart(request)
    #print('\n\n',cart)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial ={'quantity':item['quantity'], 'update' : True})
    return render(request, 'cart/detail.html', {'cart': cart})

