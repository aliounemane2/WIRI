from django.conf.urls import url
from users.views import *
from chatroom.views import *
from chatroom import views as myapp_views


urlpatterns = [
    url(r'^$', MessageList.as_view()),
    url(r'^group/$', ChatGroupList.as_view()),
    url(r'^media/$', MediaList.as_view()),
    url(r'^messages/$', MessageList.as_view()),
    url(r'^getGroupList/$', myapp_views.getGroupList, name='getGroupList'),
    url(r'^addUserGroup/$', myapp_views.addUserGroup, name='addUserGroup'),
    url(r'^addGroup/$', myapp_views.addGroup, name='addGroup'),
    url(r'^addGroup2/$', myapp_views.addGroup2, name='addGroup2'),
    url(r'^addPhotos/$', myapp_views.addPhotos, name='addPhotos'),
    url(r'^sendMessage/$', myapp_views.sendMessage, name='sendMessage'),
    url(r'^getAllMessages/$', myapp_views.getAllMessages, name='getAllMessages'),
    url(r'^delete_groups/$', myapp_views.delete_groups, name='delete_groups'),
    url(r'^get_members_groups/$', myapp_views.get_members_groups, name='get_members_groups'),
]
