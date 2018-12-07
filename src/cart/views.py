from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product

def cart_home(request): 
	# print(dir(request.session))
	if not request.session or not request.session.session_key:
		request.session.save()
	print(request.session.session_key)
	print("AAAAAAAAAAAAAAAA")
	cart_obj = Cart.objects.get_cart(request)
	context = {
	"cart": cart_obj,
	}
	return render(request,'cart.html', context)   

def cart_update(request):
	cart_obj = Cart.objects.get_cart(request)
	if cart_obj is None:
		cart_obj = Cart.objects.new_cart(request)
	product_id = request.POST.get('product_id')
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:			
			print("Ha ocurrido un error")
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
		else:
			cart_obj.products.add(product_obj)	
		request.session['cart_items'] = cart_obj.products.count()
	return redirect("cart:home")
