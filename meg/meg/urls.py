from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls', namespace='Home')),
    path('logs/', include('logs.urls', namespace='App')),
]
