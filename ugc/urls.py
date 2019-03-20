from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'api/ugc/$',views.Ugc.as_view(), name='ugc'),
	url(r'api/ugc/likes/$',views.Ugclikes.as_view(), name='ugc-likes'),
	url(r'api/ugc/comment/$',views.UgcComment.as_view(), name='ugc-comment'),
	url(r'api/ugc/comment/like/$',views.UgcCommentLike.as_view(), name='ugc-commentlike'),
	url(r'api/ugc/report/$',views.UGCReportView.as_view(),name='ugc-report'),
]