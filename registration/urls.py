from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'api/users/$', views.UserCreate.as_view(), name='registration-create'),
    url(r'api/users/forgot_password$', views.forgot_password, name='forgot_password'),
    url(r'api/users/reset_password$', views.reset_password, name='reset_password'),
	url(r'api/users/login/$',views.Login.as_view(), name='login'),
    url(r'api/users/logout/$',views.Logout.as_view(), name='logout'),
]