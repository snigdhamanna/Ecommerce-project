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
    product = Product.objects.get(id=product_id)
    product_variations = []

    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variations.append(variation)

            except Variation.DoesNotExist:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    cart.save()

    is_cart_item_exists = CartItem.objects.filter(
        product=product,
        cart=cart
    ).exists()

    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(
            product=product,
            cart=cart
        )

        ex_variations_list = []
        item_ids = []

        for item in cart_item:
            existing_variations = item.variations.all()

            ex_variations_list.append(list(existing_variations))
            item_ids.append(item.id)

        if product_variations in ex_variations_list:
            index = ex_variations_list.index(product_variations)
            item_id = item_ids[index]

            item = CartItem.objects.get(
                product=product,
                id=item_id
            )

            item.quantity += 1
            item.save()

        else:
            item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1
            )

            if len(product_variations) > 0:
                item.variations.add(*product_variations)

            item.save()

    else:

        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )

        if len(product_variations) > 0:
            cart_item.variations.add(*product_variations)

        cart_item.save()

    return redirect("cart")


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



def remove_cart(request , product_id , cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = Product.objects.get(id = product_id)
    try:
        cartitem = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cartitem.quantity > 1:
            cartitem.quantity -= 1
            cartitem.save()
        else:
            cartitem.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request , product_id , cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = Product.objects.get(id = product_id)
    try:
        cartitem = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cartitem.delete()
    except:
        pass
    return redirect('cart')
    