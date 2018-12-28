from django.shortcuts import render, redirect
from .models import Cart
from .models import Entry
from products.models import Product
from django.core.serializers.json import DjangoJSONEncoder
import json
import numpy as np


def cart_home(request):
    cart = Cart.objects.get_cart(request)
    if isinstance(cart, dict):
        total = 0
        cart_session = {}
        for key, value in cart.items():
            cart_session[Product.objects.get(id=key)] = value
            total += Product.objects.get(id=key).price * value
        context = {
            "cart": cart_session,
            "total": total,
        }
    else:
        context = {
            "cart": cart,
        }
    return render(request, "cart.html", context)


def cart_update(request):
    cart = Cart.objects.get_cart(request)
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("error, product does not exist anymore")
            return redirect('home')

        if isinstance(cart, dict):
            # if its a session based cart
            pass
            '''
            # Idea for viewed items and working with data analysis
            
            
            
            
            cart_session = request.session["cart_session"]
           
            if product_id not in cart:
                cart[product_id] = quantity
                cart_session.insert(0, [])
                cart_session[0].append(product_obj.id)
                cart_session[0].append(product_obj.title)
                cart_session[0].append(json.dumps(product_obj.price, cls=DjangoJSONEncoder))
                cart_session[0].append(quantity)
            else:
                cart[product_id] += quantity
                cart_array = np.array(cart_session)
                if str(product_obj.id) in cart_array[:, 0]:
                    # Slicing in the lists to find out if there's already the cart id
                    index_cart = cart_array[:, 0].tolist().index(str(product_obj.id))
                    cart_session[index_cart][3] = cart[str(product_id)]
                    # Assigns the value of the dict (the quantity of items)
             '''
        else:  # it is a cart object
            cart.products.add(product_obj)
            Entry.objects.create(product=product_obj, cart=cart, quantity=quantity)
            request.session['cart_items'] = len(cart.products.all())
            print(request.session['cart_items'])
    return redirect('cart:home')


"""
        

Cambios por hacer, mañana:

Agregar una vista para eliminacion de items, el update 
solo modificara o en dado caso añadira elementos al carrito
en el llamado a delete se eliminaran todos, porque en el update
se actualizaran los elementos a comprar


los elementos vistos en una lista, cuando se cierra sesion se borra
todos esos datos pero siguen allí en tu usuario.

Si es posible: 

Terminar el checkout, direcciones y demás.

Más adelate:

Mejorar las busquedas, "quizas quiso decir"


Ideas para control panel:

-Hacer una funcion que elimine los productos vistos.

- historial de compras

crear un api para integracion del frontend (react)


"""
