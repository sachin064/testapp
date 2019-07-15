from django.urls import path, re_path
from . import views

urlpatterns = [
    path('we-are-hiring/', views.hiring, name='we-are-hiring'),
    
]
