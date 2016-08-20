"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns, include
from django.contrib import admin
from preview import views
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', views.home, name='home'),
    url(r'^', include('catalog.urls')),
    url(r'^cart/', include('shoppingcart.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),


]
handler404= 'ecommerce.views.file_not_found'
