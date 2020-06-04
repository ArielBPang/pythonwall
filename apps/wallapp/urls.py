from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^welcome$', views.welcome),
    url(r'^user/register$', views.register),
    url(r'^user/login$', views.login),
    url(r'^user/logout$', views.logout),
    url(r'^wall/message$', views.message),
    url(r'^wall/comment$', views.comment),
    url(r'^wall/(?P<message_id>\d+)/like$', views.messagelike),
    url(r'^wall/(?P<message_id>\d+)/unlike$', views.messageunlike),
    url(r'^wall/comment/(?P<comment_id>\d+)/like$', views.commentlike),
    url(r'^wall/comment/(?P<comment_id>\d+)/unlike$', views.commentunlike),
    url(r'^delete/message/(?P<message_id>\d+)$', views.delete_message),
    url(r'^delete/comment/(?P<comment_id>\d+)$', views.delete_comment)
]
