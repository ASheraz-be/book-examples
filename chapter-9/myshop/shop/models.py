from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields

# TranslatableModel
class Category(models.Model):
	# translations = TranslatedFields(
	# name = models.CharField(max_length=200, db_index=True),
	# slug = models.SlugField(max_length=200, unique=True)
	# )
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, unique=True)
	
	class Meta:
		# ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
	# translations = TranslatedFields(
	# name = models.CharField(max_length=200, db_index=True),
	# slug = models.SlugField(max_length=200, unique=True),
	# description = models.TextField(blank=True),
	# )
	category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

	# Always use DecimalField to store monetary amounts. 
	price = models.DecimalField(max_digits=10, decimal_places=2)
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'),)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_detail', args=[self.id, self.slug])
