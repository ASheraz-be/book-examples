from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	# using my own UserLoginView
	path('login/', views.UserLoginView.as_view(), name='login'),

	# Using built-in class based views
	# path('login/', auth_views.LoginView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),

	# Dashboard after login
	path('', views.dashboard, name='dashboard'),

	# Update Password
	# "PasswordChangeView" view will handle the form to change the password
	path('modify_password/', auth_views.PasswordChangeView.as_view(), name='modify_password'),
	# "PasswordChangeDoneView" view will display a success message after the user has successfully changed their password
	path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),


	# Password reset views
	# path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
	# path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	# path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	# path('reset/done/',auth_views.PasswordResetCompleteView.as_view(), name='reset_done'),

	# Password reset view built-in URL provided by django
	path('', include('django.contrib.auth.urls')),

	# Register User
	path('register/', views.UserRegistrationView.as_view(), name='register_user'),

	# User & Profile Edit URL
	path('edit/', views.EditFormView, name='edit'),
]

