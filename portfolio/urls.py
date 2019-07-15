from django.urls import path, re_path
from . import views

urlpatterns = [
    path('portfolio/', views.portfolio, name='portfolio'),
    path('partners/', views.partners, name='partners'),
]
