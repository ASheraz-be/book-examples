from . import views
from django.urls import path, include

app_name = 'images'

urlpatterns = [
	path('add_image/',views.ImageView.as_view(),name='AddImage'),
	path('detail/<int:id>/<slug:slug>/',views.image_detail, name='detail'),
	path('like/', views.ajax_image_like, name='like'),
	path('', views.image_list, name='list'),
]