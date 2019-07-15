from django.conf.urls import url
from django.urls import path, include

# from import settings
from .views import signup, get_message, activate, login_view, forget_password, password, newpassword, wallet, \
    confirm_otp, reset_paswoord, user_data,logout_view
urlpatterns = [
    path('accounts/register/', signup, name='register'),
    path('accounts/wallet/', wallet, name='wallet'),
    path('loc/get-message/', get_message),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate,
        name='activate'),
    path('accounts/logine/', login_view, name='logine'),
    path('forget_password/', forget_password, name='forget_password'),
    url(r'^password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password,
        name='password'),
    url(r'^newpassword/([0-9]*)/$', newpassword, name='newpassword'),
    url(r'confirm_otp/(?P<otp>[0-9]*)/$', confirm_otp, name='confirm_otp'),
    path('reset_paswoord/', reset_paswoord, name='resetpassword'),
    path('user-data/<int:id>', user_data, name="user-data"),
    path('logout/',logout_view,name="logout")
]
