from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=140)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	# user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_of_birth = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
	phone_number = PhoneNumberField()
		
	def __str__(self):
		return f'Username: {self.user.username}'

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
    # instance.profile.save()