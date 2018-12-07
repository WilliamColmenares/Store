"""refrigeraciones URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from .views import home_page, about_page, contact_page, login_page, register_page
from products.views import detail_product, search_view
from products.models import Product, Category
from cart.views import cart_home
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('acerca/', about_page),
    path('registro/', register_page),
    path('contacto/', contact_page),
    path('ingresar/', login_page),
    path('bootstrap/', TemplateView.as_view(template_name='bootstrap/example.html')),
    path('productos/', include(('products.urls', "products"), namespace="products")),
    re_path(r'^item_(?P<slug>[\w-]+)/$', detail_product, {"object": Product}, name='detail'),
    path('search/', search_view, name='query' ),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)