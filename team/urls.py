from django.urls import path, re_path
from . import views

urlpatterns = [
    path('team/', views.team, name='team'),
]
