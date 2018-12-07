from django.urls import path, re_path
from .views import category_list, detail_product
from .models import Product, Category

urlpatterns = [
    path('paraelhogar/', category_list, {"model": Category, "name": "Home & Garden"}),
    path('vehiculos/', category_list, {"model": Category, "name": "Motors"}),
    path('moda/', category_list, {"model": Category, "name": "Fashion"}),
]