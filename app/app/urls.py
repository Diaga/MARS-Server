"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, reverse

from django.conf.urls.static import static
from django.conf import settings

from rest_framework.response import Response
from rest_framework.routers import DefaultRouter, APIRootView


class MARSAPIRootView(APIRootView):
    """Custom API root view for MARS"""

    @staticmethod
    def get_url(request, url):
        """Return dynamic hyperlink"""
        return f'http://{request.get_host()}{url}'

    def get(self, request, *args, **kwargs):
        """Return custom dict containing all methods"""
        res = {
            'user-view': self.get_url(request, reverse('user:user-view')),
        }

        return Response(res)


class Router(DefaultRouter):
    """Custom router for MARS"""
    root_view_name = 'mars-api-root'
    APIRootView = MARSAPIRootView
    routes = []


router = Router()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),
    path('api/', include('record.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
