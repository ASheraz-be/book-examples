from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
	# post views

	# Tag with Simple View
	# path('', views.post_list, name='post_list'),
	# path('slug/<slug:slug_val>/', views.post_list, name='post_list_tag')

	path('<int:post_id>/share/', views.post_share, name='post_share'),
	
	path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail, name='post_detail'),
	
	# Tag with Class Based List View
	path('', views.PostListView.as_view(), name='post_list'),
	path('slug/<slug:slug_val>/', views.PostListView.as_view(), name='post_list_tag'),

	# Search with Simple View
	# path('search/', views.post_search, name='post_search'),

	# Search with Class based FormView
	path('search/', views.PostSearchView.as_view(), name='post_search'),
]