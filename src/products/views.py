from django.shortcuts import render
from django.http import Http404
from .models import Product
from cart.models import Cart


def category_list(request, **kwargs):
    model = kwargs.get('model')
    name = kwargs.get('name')
    queryset = model.objects.get(name=name).product_set.all()
    context = {
        "category": name,
        "object": queryset,
    }
    return render(request, 'category.html', context)


def search_view(request):
    search_query = request.GET.get('q', None)
    if search_query is not None:
        queryset = Product.objects.search(search_query)
    else:
        queryset = Product.objects.none()
    context = {
        "object": queryset,
    }
    return render(request, 'category.html', context)


def detail_product(request, **kwargs):
    cart_obj = Cart.objects.get_cart(request)
    model = kwargs.get('object')
    slug = kwargs.get('slug')
    try:
        instance = model.objects.get(slug=slug)
    except model.DoesNotExist:
        raise Http404("NO ENCONTRADO")
    context = {
        "object": instance,
        "cart": cart_obj,
    }
    return render(request, 'detalle.html', context)
