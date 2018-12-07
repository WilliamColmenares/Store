from django.db import models
import os, random
from django.db.models.signals import pre_save
from products.utils import slug_generator
from django.urls import reverse
from django.db.models import Q


def get_file_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_image(obj_instance, filename):
	new_filename		= random.randint(434253412332452,98489342983479723498234834348534345233410)
	name, ext 			= get_file_ext(filename)
	final_filename 		= 'products/{}/{}{}'.format(obj_instance.reference, new_filename, ext) 
	return final_filename

class ProductsQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(is_active=True)
	def category(self):
		return self.category
	def search(self, query):
		qs = Q(title__icontains=query) | Q(description__icontains=query)
		return self.filter(qs).distinct() 	

class ProductsManager(models.Manager):
	def get_queryset(self):
		return ProductsQuerySet(self.model)
	def toyota(self):
		return self.get_queryset().filter(brand="Toyota")
	def featured(self):
		return self.get_queryset().filter(featured=True)
	def all(self):
		return self.get_queryset().active()
	def search(self, query):
		qs = Q(title__icontains=query) | Q(description__icontains=query)
		return self.get_queryset().active().search(query)



class Category(models.Model):
	class Meta:
		verbose_name_plural = "Categories"
	name = models.CharField(max_length=120, null=True)

	def __str__(self):
		return self.name



class Product(models.Model):
	category 		= models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	title			= models.CharField(max_length=120, null=True)
	slug			= models.SlugField(null=True, unique=True, blank=True)
	brand			= models.CharField(max_length=120, null=True)
	reference		= models.CharField(max_length=20, null=True)
	description		= models.TextField()
	price			= models.DecimalField(decimal_places=2, max_digits=30, null=True)
	image_1			= models.ImageField(upload_to=upload_image, null=True)
	image_2			= models.ImageField(upload_to=upload_image, null=True, blank=True)
	image_3			= models.ImageField(upload_to=upload_image, null=True, blank=True)
	image_4			= models.ImageField(upload_to=upload_image, null=True, blank=True)
	image_5			= models.ImageField(upload_to=upload_image, null=True, blank=True)
	image_6			= models.ImageField(upload_to=upload_image, null=True, blank=True)
	image_7			= models.ImageField(upload_to=upload_image, null=True, blank=True)
	image_8			= models.ImageField(upload_to=upload_image, null=True, blank=True)
	objects			= ProductsManager()
	featured		= models.BooleanField(default=False)
	is_active		= models.BooleanField(default=False)


	def __str__(self):
		return '%s. (%s Bs.). Artículo de %s' % (self.title, self.price, self.category)

	def get_absolute_url(self):
		return reverse("detail", kwargs={"slug": self.slug})


def products_pre_save(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slug_generator(instance)

pre_save.connect(products_pre_save, sender=Product)