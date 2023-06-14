from django.urls import path
from . import views
from .forms import ReadFileForm

app_name = 'App'

urlpatterns = [
    path('system/<int:id>/', views.system, name='system'),
    path('parse_file/', views.parse_file, name='parcer'),
]
