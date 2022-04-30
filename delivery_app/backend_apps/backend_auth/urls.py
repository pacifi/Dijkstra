from django.conf.urls import url

from .views.group import GroupListView, GroupCretaView, GroupUpdateView, GroupDeleteView
from .views.menu import MenuUpdateActiveView, MenuUpdateView, MenuDeleteView
from .views.user import UserCreateView, UserUpdateView, UserDeleteView
from .views.group_permission import GroupPermissionsUpdateView

from .views.user import (UserListView)
from .views.menu import (MenuListView, MenuCreateView)
from .views.permission import (PermissionCreateView, PermissionDeleteView, PermissionListView,
                               PermissionUpdateView)

urlpatterns = [

    # User
    url(r'^user/list/$', UserListView.as_view(), name='user_list'),
    url(r'^user/add/$', UserCreateView.as_view(), name='user_add'),
    url(r'^user/update/(?P<pk>[^/]+)/$', UserUpdateView.as_view(), name='user_update'),
    url(r'^user/delete/(?P<pk>[^/]+)/$', UserDeleteView.as_view(), name='user_delete'),

    url(r'^group/list/$', GroupListView.as_view(), name='group_list'),
    url(r'^group/add/$', GroupCretaView.as_view(), name='group_add'),
    url(r'^group/update/(?P<pk>[^/]+)/$', GroupUpdateView.as_view(), name='group_update'),
    url(r'^group/delete/(?P<pk>[^/]+)/$', GroupDeleteView.as_view(), name='group_delete'),
    url(r'^grouppermissions/update/$', GroupPermissionsUpdateView.as_view(), name='group_permissions_update'),

    # Menu
    url(r'^menu/list/$', MenuListView.as_view(), name='menu_list'),
    url(r'^menu/add/$', MenuCreateView.as_view(), name='menu_add'),
    url(r'^menu/state/(?P<state>[\w\d\-]+)/(?P<pk>[^/]+)/$',
        MenuUpdateActiveView.as_view(), name='menu_state'),
    url(r'^menu/update/(?P<pk>[^/]+)/$', MenuUpdateView.as_view(), name='menu_update'),
    url(r'^menu/delete/(?P<pk>[^/]+)/$', MenuDeleteView.as_view(), name='menu_delete'),

    #
    url(r'^permission/delete/(?P<pk>.*)/$',
        PermissionDeleteView.as_view(), name='permission_delete'),  # x pony
    url(r'^permission/update/(?P<pk>.*)/$',
        PermissionUpdateView.as_view(), name='permission_update'),
    url(r'^permission/add/$',
        PermissionCreateView.as_view(), name='permission_add'),
    url(r'^permission/list/$',
        PermissionListView.as_view(), name='permission_list'),

]
