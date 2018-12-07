from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save, m2m_changed

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
	def get_cart(self, request):
		"""Get the cart based on the curret session"""
		cart_id = request.session.get("cart_id", None)
		lookup = self.get_queryset().filter(id=cart_id)
		if lookup.count() == 1:
			cart_obj = lookup.first()
			if request.user.is_authenticated and cart_obj.user is None:
				cart_obj.user = request.user
				cart_obj.save()
		else:
			cart_obj = None
			# cart_obj = self.new(user=request.user)
			# request.session['cart_id'] = cart_obj.id
			# new_obj = True
		return cart_obj

	def new_cart(self, request):
		"""Creates a new cart object"""
		user_obj = None
		user = request.user
		if user is not None:
			if user.is_authenticated:
				user_obj = user
			cart_obj = self.model.objects.create(user=user_obj)
		request.session['cart_id'] = cart_obj.id
		return cart_obj

class Cart(models.Model):
	user 		= models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	products	= models.ManyToManyField(Product, blank=True)
	total 		= models.DecimalField(default=0.00, max_digits=10000, decimal_places=2)
	updated 	= models.DateTimeField(auto_now=True)
	created 	= models.DateTimeField(auto_now_add=True)
	objects		= CartManager()

	def __str__(self):
		return str(self.id)




def m2m_changed_cart(sender, instance, action, *args, **kwargs):
	products = instance.products.all()
	total = 0
	for x in products:
		total+=x.price
	instance.total = total
	instance.save()
m2m_changed.connect(m2m_changed_cart, sender=Cart.products.through)	








