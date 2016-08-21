from  django.shortcuts import render, render_to_response, get_object_or_404
# Create your views here.

def home(request):
    return render_to_response('index.html')
