from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'api/correction/$', views.GameCorrection.as_view(), name='game-correction'),
    url(r'api/user/auth_status/$', views.user_auth_status, name='user-auth-status'),
	url(r'api/user/follow/$',views.UserFollow.as_view(), name='follow-user'),
	url(r'api/game/rating/$',views.GameRating.as_view(), name='game-rating'),
]