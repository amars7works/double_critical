from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'api/game/correction/$', views.GameCorrection.as_view(), name='game-correction'),
	url(r'api/game/rating/$',views.GameRating.as_view(), name='game-rating'),
	url(r'api/game/follow/$',views.GameFollow.as_view(), name='game-follow'),
	url(r'api/game/collection/$',views.CollectingGame.as_view(), name='game-collection'),
	url(r'api/game/$',views.CreateGame.as_view(), name='create-game'),
	url(r'api/game/trending/$',views.TrendingGames.as_view(), name='trending-games'),
	url(r'api/game/likes/$',views.LikeGames.as_view(), name='like-games'),
	url(r'api/game/following/feed/$',views.GameFollowingFeed.as_view(), name='game-following-feed'),
	# url(r'api/game/following/feed/list/$',views.GameFollowingFeedList.as_view(), name='game-following-feed-list'),
	# url(r'api/user/following/feed/$',views.UserFollowingFeed.as_view(), name='user-following-feed'),
	url(r'api/game/common/$',views.UserCommonGame.as_view(), name='common-games'),
	url(r'api/game/barcode/$',views.BarCode.as_view(), name='barcode-game'),
	url(r'api/game/increment/like/$',views.incement_like_count.as_view(), name='inc-like-game'),
	url(r'api/game/feed/$',views.GameFeeds.as_view(), name='feed-game'),
	url(r'api/game/feed/comment/$',views.GameComments.as_view(), name='feed-comment-game'),
	url(r'api/game/feed/commentlike/$',views.GameCommentLike.as_view(), name='feed-commentlike-game'),
	url(r'api/game/feed/comment/replay/$',views.GameCommentsReplay.as_view(), name='feed-comment-replay-game'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)