# project/urls.py
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('application.urls')),
     
     ]+ debug_toolbar_urls()


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)