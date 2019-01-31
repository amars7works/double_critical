from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'api/users/$', views.UserCreate.as_view(), name='registration-create'),
	url(r'api/users/login/$',views.Login.as_view(), name='login'),
    url(r'api/users/logout/$',views.Logout.as_view(), name='logout'),
]