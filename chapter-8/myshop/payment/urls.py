from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
	path('process/', views.payment_process, name='process'),
	# path('done/', views.PaymentDone.as_view(), name='done'),
	# path('canceled/', views.PaymentCanceled.as_view(), name='canceled'),

	path('done/', views.payment_done, name='done'),
	path('canceled/', views.payment_canceled, name='canceled'),
]