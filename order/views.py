from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from product.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit= False)
            order.user = request.user.id
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            

            # Buyer Mail Sending
            subject = f"Hi {request.user}!"
            message = f"Your Product order placed successfully \nYour order Id is {order.id} \n\n\t Thank you for using \'Resale Portal\'"
            to_mail = request.user.email
            send_mail (subject, message, settings.EMAIL_HOST_USER,[to_mail],fail_silently=False)
            
            # Sellers mail Sending
            for item in cart:
                cart_product = Product.objects.get(name = item['product'])
                selleruser = User.objects.get(id = cart_product.owner_id)
                #print(item['product'], cart_product,selleruser.email)
                subject = f"Hi {selleruser}!"
                message = f"Your product {cart_product} is orderd by {request.user} \n\nOrder Details:\nProduct Name: {item['product']}\nQuantity: {item['quantity']}\nUnit Price: {item['price']}\nTotal Price: {item['price']*item['quantity']}."
                to_mail = selleruser.email
                send_mail(subject, message, settings.EMAIL_HOST_USER, [to_mail], fail_silently= False)
            
            # clear the cart
            cart.clear()
            
            return render(request, 'order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})


@login_required
def order_list(request):
    #print("\t\t",request.user.id)
    orderlist = Order.objects.filter(user = request.user.id)
    #print("\t\t",orderlist,Order.get_total_cost(orderlist))
    order_total_price = OrderItem.objects.filter(order = orderlist)
    #print("\t\t",orderlist)
    return render(request,'order/orderlist.html',{'orderlist':orderlist,'order_total_price':order_total_price})

@login_required
def order_cancel(request,order_id):
    order = Order.objects.get(id = order_id)
    #print("\t\t",order)
    order.delete()
    messages.warning(request,"Order Cancelled Successfully.")
    return redirect("/orders/list")