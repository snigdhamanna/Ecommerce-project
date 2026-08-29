from django.shortcuts import render , redirect
from .models import *
from store.models import *
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart = cart)
        cart_item.quantity += 1
        
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product, cart = cart , quantity = 1)
        
    cart_item.save()
    
    return redirect ('cart')




def cart(request , total=0 , quantity=0 ,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id =_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
        tax = (2 * total)/100
        grand_total = tax+total
    except ObjectDoesNotExist:
        pass
    context ={
        'quantity':quantity,
        'total':total,
        'cart_items': cart_items   ,
        'tax':tax,
        'grand_total':grand_total,
        
        }
        
    return render(request, 'store/cart.html',context)



def remove_cart(request , product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = Product.objects.get(id = product_id)
    cartitem = CartItem.objects.get(product=product, cart=cart)
    if cartitem.quantity > 1:
        cartitem.quantity -= 1
        cartitem.save()
    else:
        cartitem.delete()
    return redirect('cart')

def remove_cart_item(request , product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = Product.objects.get(id = product_id)
    cartitem = CartItem.objects.get(product=product, cart=cart)
    cartitem.delete()
    return redirect('cart')
    