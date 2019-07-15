from django.conf.urls import url
from django.urls import path, include
from .views import home,about

urlpatterns = [
    path('',home, name='home'),
    path('',about,name='about'),
]