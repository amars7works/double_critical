from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'api/correction/$', views.GameCorrection.as_view(), name='game-correction'),
    url(r'api/user/auth_status/$', views.user_auth_status, name='user-auth-status'),
]