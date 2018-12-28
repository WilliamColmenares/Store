from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import m2m_changed

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
	def get_cart(self, request):
		"""Get the cart based on the current session or the user"""
		if request.user.is_authenticated:
			lookup = self.model.objects.filter(user=request.user)
			if lookup.count() > 0:
				cart = lookup.first()
				if cart.user is None:
					cart.user = request.user
					cart.save()
			else:
				cart = self.new_cart(request)
		else:
			if not request.session or not request.session.session_key:
				request.session.save()
				request.session["items"] = {}
				request.session["cart_session"] = []
			cart = request.session["items"]
		return cart

	def new_cart(self, request):
		"""Creates a new cart object"""
		cart = self.model.objects.create(user=request.user)
		return cart


class Cart(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	products = models.ManyToManyField(Product, blank=True)
	total = models.DecimalField(default=0.00, max_digits=10000, decimal_places=2)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	objects = CartManager()

	def __str__(self):
		return str(self.id)


class Entry(models.Model):
	class Meta:
		verbose_name_plural = "Entries"
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
	quantity = models.PositiveIntegerField(default=1)


def m2m_changed_cart(sender, instance, action, *args, **kwargs):
	products = instance.products.all()
	total = 0
	for x in products:
		total += x.price
	instance.total = total
	instance.save()


m2m_changed.connect(m2m_changed_cart, sender=Cart.products.through)	








