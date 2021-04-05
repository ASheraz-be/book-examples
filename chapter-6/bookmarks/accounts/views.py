from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegisterationForm, UserEditForm, ProfileEditForm
from .models import Profile, MyUser, Contact
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView, View
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.http import HttpResponse
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required_decorator
# from django.contrib.auth.views import LoginView
# import sys, os, inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)
# print(parentdir)
from actions.utils import create_action
from actions.models import Action

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
	# Display all actions by default
	actions = Action.objects.exclude(user=request.user)
	following_ids = request.user.following.values_list('id',flat=True)
	if following_ids:
		# If user is following others, retrieve only their actions
		actions = actions.filter(user_id__in=following_ids)
		# actions = actions[:10]

		# select_related() carefully can vastly improve execution time.
		actions = actions.select_related('user', 'user__profile')[:10]
	return render(request, 'accounts/dashboard.html', {'section': 'dashboard','actions': actions})
	# return render(request,
	# 	'accounts/dashboard.html',
	# 	{'section': 'dashboard'})

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
			create_action(new_user, 'has created an account')
			return render(request, self.template_name, {'form': new_user})
		else:
			messages.error(request, 'Username or Email already exits.')

		return render(request, self.template_name, {'form': self.form_class})

@method_decorator(login_required, name='dispatch')
class UserList(ListView):
	template_name = 'accounts/user/list.html'
	def get(self, request, *args, **kwargs):
		users = MyUser.objects.filter(is_active=True)
		return render(request, self.template_name, {'section': 'people', 'users': users})

@method_decorator(login_required, name='dispatch')
class UserDetail(DetailView):
	template_name = 'accounts/user/detail.html'

	def get(self, request, *args, **kwargs):
		user = get_object_or_404(MyUser, username=kwargs['username'], is_active=True)
		return render(request, self.template_name, {'section': 'people', 'user': user})


@ajax_required_decorator
@require_POST
@login_required
def user_follow(request):
	user_id = request.POST.get('id')
	action = request.POST.get('action')
	if user_id and action:
		try:
			user = MyUser.objects.get(id=user_id)
			if action == 'follow':
				Contact.objects.get_or_create(user_from=request.user,user_to=user)
				create_action(request.user, 'is following', user)
			else:
				Contact.objects.filter(user_from=request.user, user_to=user).delete()
			return JsonResponse({'status':'ok'})
		except MyUser.DoesNotExist:
			return JsonResponse({'status':'error'})
	return JsonResponse({'status':'error'})


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
