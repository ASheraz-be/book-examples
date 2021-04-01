from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegisterationForm, UserEditForm, ProfileEditForm
from .models import Profile, MyUser
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView, View
from django.http import HttpResponse
from django.contrib import messages
# from django.contrib.auth.views import LoginView

# authenticate() checks user credentials and returns a User object if they are correct; 
# login() sets the user in the current session
class UserLoginView(FormView):
	form_class = LoginForm
	template_name = 'registration/login.html'

	def post(self, request, *args, **kwargs):
		form = self.form_class(self.request.POST)
		if form.is_valid():
			clean_data = form.cleaned_data
			print(clean_data)
			user_auth = authenticate(request, email=clean_data['email'], password=clean_data['password'])
			if user_auth is not None:
				if user_auth.is_active:
					login(request, user_auth)
					return render(request,'accounts/dashboard.html',{'section': 'dashboard'})
				else:
					messages.error(request, 'User is not active.')
					return render(request, self.template_name, {'form': self.form_class})
			else:
				messages.error(request, 'Login failed, Email or Password is incorrect.')
				return render(request, self.template_name, {'form': self.form_class})
		return render(request, self.template_name, {'form': self.form_class})

@login_required
def EditFormView(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Profile updated successfully')
		else:
			messages.error(request, 'Profile update failed')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)
		
	return render(request,'accounts/edit.html',{'user_form': user_form,'profile_form': profile_form})

@login_required
def dashboard(request):
	return render(request,
		'accounts/dashboard.html',
		{'section': 'dashboard'})

class UserRegistrationView(FormView):
	form_class = UserRegisterationForm
	template_name = 'accounts/register.html'


	def post(self, request, *args, **kwargs):
		form = self.form_class(self.request.POST)
		if form.is_valid():
			clean_data = form.cleaned_data
			new_user = form.save(commit=False)
			new_user.set_password(clean_data['password'])
			new_user.save()
			Profile.objects.create(user=new_user)
			return render(request, self.template_name, {'form': new_user})
		else:
			messages.error(request, 'Username or Email already exits.')

		return render(request, self.template_name, {'form': self.form_class})

# @login_required
# class EditFormView(View):
# 	template_name = 'accounts/edit.html'
# 	form_classes = {'user_form': UserEditForm,
#                     'profile_form': ProfileEditForm}

# 	def post(self, request):
# 		if request.POST:
# 			user_form = UserEditForm(request.POST)
# 			profile_form = ProfileEditForm(request.POST)

# 			if user_form.is_valid() and profile_form.is_valid():
# 				user_form.save()
# 				profile_form.save()
			
# 		return render(request, self.template_name, {"user_form":user_form, "profile_form":profile_form})
