"""bookmarks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from accounts.urls import urlpatterns as url_accounts
from django.conf import settings
from django.conf.urls.static import static
# import images.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(url_accounts)),

    # Several social services will not allow redirecting users to 127.0.0.1 or localhost after a successful authentication; they expect a domain name.
    path('social-media-auth/', include('social_django.urls', namespace='social')),
    path('images/', include('images.urls', namespace='images')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)