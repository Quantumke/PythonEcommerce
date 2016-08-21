from xml.dom.minidom import Document
from xml.dom import minidom
from django.http import HttpRequest, HttpResponseRedirect
from django.conf import settings
from urllib2 import Request, urlopen, HTTPError, URLError
import base64
import  ssl

from shoppingcart.models import CartItem
from shoppingcart import cart

def get_check_out_url(request):
    redirect_url=''
    req=_create_mpesa_checkout_request(request)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    try:
        response_xml=urlopen(req, context=context).read()
        print(response_xml)
    except HTTPError, err:
        raise err
    except URLError, err:
        raise err
    else:
        redirect_url=_parse_saf_checkout_response(response_xml)
    return redirect_url

def _create_mpesa_checkout_request(request):
    url=settings.CHECKOUT_URL
    cart=_build_xml_shopping_cart(request)
    req=Request(url=url, data=cart)
    merchant_key=settings.MERCHANT_TRANSACTION_ID
    merchant_password=settings.MERCHANT_PASSWORD
    key_id=merchant_key + ':' + merchant_password
    authorization_value=base64.encodestring((key_id))[:-1]
    req.add_header('Authorization', 'Basic %s' %authorization_value)
    req.add_header('Contect-Type', 'application/xml; charset=UTF-8' )
    req.add_header('Accept','application/xml; charset=UTF-8')
    return req
def _parse_saf_checkout_response(response_xml):
    redirect_url=''
    xml_doc=minidom.parseString(response_xml)
    root= xml_doc.documentElement
    node=root.childNodes[1]
    if node.tagname == 'redirect-url':
        redirect_url = node.firstchild.data
    if node.tagname == 'error-message':
        raise  RuntimeError(node.firstchild.data)
    return redirect_url

def _build_xml_shopping_cart(request):
    doc= Document()
    root= doc.createElement('checkout-shopping-cart')
    root.setAttribute('xmlns', settings.CHECKOUT_URL)
    doc.appendChild(root)
    shopping_cart= doc.createElement('shopping_cart')
    root.appendChild(shopping_cart)
    items= doc.createElement('items')
    shopping_cart.appendChild(items)

    cart_items= cart.get_cart_items(request)
    for cart_item in cart_items:
        item=doc.createElement('item')
        items.appendChild(item)

        MERCHANT_TRANSACTION_ID = doc.createElement('MERCHANT_TRANSACTION_ID')
        MERCHANT_TRANSACTION_ID_TEXT = doc.createTextNode(settings.MERCHANT_TRANSACTION_ID)
        MERCHANT_TRANSACTION_ID.appendChild(MERCHANT_TRANSACTION_ID_TEXT)
        item.appendChild(MERCHANT_TRANSACTION_ID)

        MSISDN = doc.createElement('MERCHANT_TRANSACTION_ID')
        MSISDN_TEXT = doc.createTextNode(str('0721799582'))
        MSISDN.appendChild(MSISDN_TEXT)
        item.appendChild(MSISDN)

        REFERENCE_ID = doc.createElement('REFERENCE_ID')
        REFERENCE_ID_TEXT = doc.createTextNode(str('2016820160721799582'))
        REFERENCE_ID.appendChild(REFERENCE_ID_TEXT)
        item.appendChild(REFERENCE_ID)

        ENC_PARAMS = doc.createElement('ENC_PARAMS')
        ENC_PARAMS_TEXT = doc.createTextNode(str('2016820160721799582'))
        ENC_PARAMS.appendChild(ENC_PARAMS_TEXT)
        item.appendChild(ENC_PARAMS)

        AMOUNT = doc.createElement('AMOUNT')
        AMOUNT_TEXT = doc.createTextNode(str(cart_item.price))
        AMOUNT.appendChild(AMOUNT_TEXT)
        item.appendChild(AMOUNT)

        CALL_BACK_URL = doc.createElement('CALL_BACK_URL')
        CALL_BACK_URL_TEXT = doc.createTextNode(str(settings.CALL_BACK_URL))
        CALL_BACK_URL.appendChild(CALL_BACK_URL_TEXT)
        item.appendChild(CALL_BACK_URL)

        CALL_BACK_METHOD = doc.createElement('CALL_BACK_METHOD')
        CALL_BACK_METHOD_TEXT = doc.createTextNode(str(settings.CALL_BACK_METHOD))
        CALL_BACK_URL.appendChild(CALL_BACK_METHOD_TEXT)
        item.appendChild(CALL_BACK_METHOD)

        TIMESTAMP = doc.createElement('TIMESTAMP')
        TIMESTAMP_TEXT = doc.createTextNode(str(settings.TIMESTAMP))
        TIMESTAMP.appendChild(TIMESTAMP_TEXT)
        item.appendChild(TIMESTAMP)

        return doc.toxml(encoding='utf-8')








