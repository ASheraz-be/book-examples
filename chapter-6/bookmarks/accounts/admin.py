from django.contrib import admin
from .models import Profile, Contact
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

admin.site.register(MyUser, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'date_of_birth', 'photo']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ['user_to', 'user_from', 'created']

