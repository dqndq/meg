from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls', namespace='Home')),
    path('logs/', include('logs.urls', namespace='App')),
]

if settings.DEBUG:
    urlpatterns += (path('__debug__/', include('debug_toolbar.urls')),)
    urlpatterns += (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
