from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'api/user/follow/$',views.UserFollow.as_view(), name='follow-user'),
	url(r'api/hotornot/swipe/$',views.HotorNotSwipe.as_view(), name='games-hotornot-swipe'),
	url(r'api/product/page/link/$',views.DiscoveryModeHotorNot.as_view(), name='discoverymode-hotornot'),
	url(r'api/discoverymode/swipe/$',views.DiscoveryModeSwipe.as_view(), name='discoverymode-swipe'),
]