from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'api/search/$',views.Search.as_view(), name='search'),
]