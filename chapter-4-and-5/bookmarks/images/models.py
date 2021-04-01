from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='image_related', on_delete=models.CASCADE)
	title = models.CharField(max_length=150)
	slug = models.SlugField(max_length=150, blank=True)
	website_name = models.CharField(max_length=150, blank=True)
	url = models.URLField()
	description = models.TextField(max_length=200, blank=True)
	created = models.DateField(auto_now_add=True, db_index=True)
	image = models.ImageField(upload_to='images/%Y/%m/%d/')

	# ManyToManyField: Django creates an intermediary join table using the primary keys of both models
	# Image.users_image_like.all()
	# User.image_liked.all()
	users_image_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='image_liked', blank=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)

		super().save(*args, **kwargs)


	def get_absolute_url(self):
		return reverse('images:detail', args=[self.id, self.slug])