from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/wallet/', views.wallet, name='wallet'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/password_reset/',auth_views.PasswordResetView.as_view(),name='admin_password_reset',),
    path('accounts/password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done',),
    path('accounts/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm',),
    path('accounts/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete',),
    #path('account_activation_sent', views.account_activation_sent, name='account_activation_sent'),
    #path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]
