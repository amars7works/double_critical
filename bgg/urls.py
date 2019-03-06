from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'api/correction/$', views.GameCorrection.as_view(), name='game-correction'),
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
	url(r'api/game/trending/$',views.TrendingGames.as_view(), name='trending-games'),
	url(r'api/game/likes/$',views.LikeGames.as_view(), name='like-games'),
	url(r'api/game/report/$',views.UGCReportView.as_view(),name='ugc-report'),
	url(r'api/game/following/feed/$',views.GameFollowingFeed.as_view(), name='following-feed'),
	url(r'api/user/following/feed/$',views.UserFollowingFeed.as_view(), name='following-feed'),
	url(r'api/hotornot/swipe/$',views.HotorNotSwipe.as_view(), name='games-hotornot-swipe'),
	url(r'api/product/page/link/$',views.DiscoveryModeHotorNot.as_view(), name='discoverymode-hotornot'),
	url(r'api/discoverymode/swipe/$',views.DiscoveryModeSwipe.as_view(), name='discoverymode-swipe'),
	url(r'api/game/common/$',views.UserCommonGame.as_view(), name='common-games'),
	url(r'api/search/$',views.Search.as_view(), name='search'),
]