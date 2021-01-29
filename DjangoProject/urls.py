"""DjangoProject URL Configuration

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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Creative web API')

admin.site.site_header = 'Creative Web Admin'
admin.site.site_title = 'Creative Web'
admin.site.site_url = 'http://creativeweb.com/'
admin.site.index_title = 'CreativeWeb administration'
admin.empty_value_display = '**Empty**'

urlpatterns = [
                  path('api/', schema_view),
                  path('auth/', include('AuthApp.urls')),
                  path('secure/', include('PostApp.urls')),
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
                  path('', include('drfpasswordless.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
