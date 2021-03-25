from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Tag is the Manager provided by "taggit" 
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,
		self).get_queryset()\
		.filter(status='published')

class DraftManager(models.Manager):
	def get_queryset(self):
		return super(DraftManager,
		self).get_queryset()\
		.filter(status='draft')

class Post(models.Model):
	STATUS_CHOICES = (
	('draft', 'Draft'),
	('published', 'Published'),
	)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250,
	unique_for_date='publish')
	author = models.ForeignKey(User,
	on_delete=models.CASCADE,
	related_name='blog_posts')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,
	choices=STATUS_CHOICES,
	default='draft')

	objects = models.Manager() # The default manager.
	published = PublishedManager() # Our custom manager.
	draft = DraftManager()
	tag = TaggableManager()

	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title



class Comments(models.Model):
	# related_name works like a manager
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	name = models.CharField(max_length=25)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	activate = models.BooleanField(default=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return f'{self.name} commented'

