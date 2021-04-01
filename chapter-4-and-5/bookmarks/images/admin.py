from django.contrib import admin
from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
	list_display = ['title','description','image','slug','created']
	list_filter = ['created']

