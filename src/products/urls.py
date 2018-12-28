from django.urls import path
from .views import category_list
from .models import Category

urlpatterns = (
    path('paraelhogar/', category_list, {"model": Category, "name": "Home & Garden"}),
    path('vehiculos/', category_list, {"model": Category, "name": "Motors"}),
    path('moda/', category_list, {"model": Category, "name": "Fashion"}),
)
