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

class Contact(models.Model):
	user_from = models.ForeignKey(MyUser, related_name='rel_from_set', on_delete=models.CASCADE)
	user_to = models.ForeignKey(MyUser, related_name='rel_to_set', on_delete=models.CASCADE)
	
	created = models.DateTimeField(auto_now_add=True, db_index=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return f'{self.user_from} follows {self.user_to}'


from django.contrib.auth import get_user_model
# Add following field to User dynamically
user_model = get_user_model()

user_model.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))