from django import forms
# from django.contrib.auth.models import User
from .models import Profile, MyUser

class ProfileEditForm(forms.ModelForm):
	# phone_number = forms.CharField(max_length=11, min_length=11)
	class Meta:
		model = Profile
		fields = ['date_of_birth', 'photo', 'phone_number']

class UserEditForm(forms.ModelForm):
	class Meta:
		model = MyUser
		fields = ['first_name', 'last_name', 'email']

class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)

class UserRegisterationForm(forms.ModelForm):
	password = forms.CharField(label='Password',widget=forms.PasswordInput)
	repeat_password = forms.CharField(label='Repeat Password',widget=forms.PasswordInput)

	class Meta:
		model = MyUser
		fields = ('username', 'first_name', 'email')

	# In this case, we use the field-specific clean_repeat_password() validation instead of overriding the clean() 
	def clean_repeat_password(self):
		clean_data = self.cleaned_data
		if clean_data['password'] != clean_data['repeat_password']:
			raise forms.ValidationException("Password does not matched!!")

		return clean_data['repeat_password']