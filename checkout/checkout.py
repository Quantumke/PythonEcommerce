import mpesa_checkout
def get_checkout_url(request):
    return mpesa_checkout.get_check_out_url(request)
