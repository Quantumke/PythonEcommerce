from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from shoppingcart import cart
from checkout import checkout
from ecommerce import settings

def show_cart(request, template_name="cart/cart.html"):
    if request.method == "POST":
        postdata= request.POST.copy()
        if postdata['submit']== 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit']== 'Update':
            cart.update_cart(request)
        if postdata['submit']=='Checkout':
            checkout_url=checkout.get_checkout_url(request)
            return  HttpResponseRedirect(checkout_url)
    cart_items= cart.get_cart_items(request)
    # cart_item_count = cart.cart_item_count(request)
    page_title = 'Shopping Cart'
    merchant_id=settings.MERCHANT_TRANSACTION_ID
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
