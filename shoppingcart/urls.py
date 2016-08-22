from django.conf.urls.defaults import  *
from django.conf.urls import url, patterns, include

urlpatterns = patterns('shoppingcart.views',
(r'^$', 'show_cart', {'template_name': 'cart/cart.html'}, 'show_cart'),
)
