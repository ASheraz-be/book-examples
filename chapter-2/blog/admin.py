from django.contrib import admin

from .models import Post, Comments

# @admin.register(Post) this decorator is equal to admin.site.register(Post) function
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'author', 'publish', 'status')
	list_filter = ('status', 'created', 'publish', 'author')
	search_fields = ('title', 'body')
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ('author',)
	date_hierarchy = 'publish'
	ordering = ('status', 'publish')

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
	list_display = ('post', 'name', 'email', 'body',  'created', 'activate')
	list_filter = ('activate', 'created')
	search_fields = ('name', 'email')