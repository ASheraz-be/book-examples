from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['date_of_birth', 'photo']

class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class UserRegisterationForm(forms.ModelForm):
	password = forms.CharField(label='Password',widget=forms.PasswordInput)
	repeat_password = forms.CharField(label='Repeat Password',widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'email')

	# In this case, we use the field-specific clean_repeat_password() validation instead of overriding the clean() 
	def clean_repeat_password(self):
		clean_data = self.cleaned_data
		if clean_data['password'] != clean_data['repeat_password']:
			raise forms.ValidationException("Password does not matched!!")

		return clean_data['repeat_password']