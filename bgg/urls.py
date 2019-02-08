from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'api/correction/$', views.GameCorrection.as_view(), name='game-correction'),
    url(r'api/user/auth_status/$', views.user_auth_status, name='user-auth-status'),
	url(r'api/user/follow/$',views.UserFollow.as_view(), name='follow-user'),
	url(r'api/game/rating/$',views.GameRating.as_view(), name='game-rating'),
	url(r'api/game/follow/$',views.GameFollow.as_view(), name='game-follow'),
	url(r'api/game/collection/$',views.CollectingGame.as_view(), name='game-collection'),
	url(r'api/ugc/$',views.Ugc.as_view(), name='ugc'),
	url(r'api/ugc/likes/$',views.Ugclikes.as_view(), name='ugc-likes'),
	url(r'api/ugc/comment/$',views.UgcComment.as_view(), name='ugc-comment'),
	url(r'api/ugc/comment/like/$',views.UgcCommentLike.as_view(), name='ugc-commentlike'),
	url(r'api/game/$',views.CreateGame.as_view(), name='create-game'),
	url(r'api/game/extension/$',views.GameExtension.as_view(), name='game-extension'),
]