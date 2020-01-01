# coding:utf-8

from django.urls import path
from .views.index import Index
from .views.auth import Login, AdminManger, Logout, UpdateAdminStatus
from .views.video import ExternalVideo, VideoSubView, VideoStarView

urlpatterns = [
    path('', Index.as_view(), name='dashboard_index'),
    path('login', Login.as_view(), name='dashboard_login'),
    path('logout', Logout.as_view(), name='dashboard_logout'),
    path('admin/manger', AdminManger.as_view(), name='dashboard_admin_manger'),
    path('admin/manger/status', UpdateAdminStatus.as_view(), name='dashboard_admin_status'),
    path('video/external', ExternalVideo.as_view(), name='external_link'),
    path('video/videosub/<int:video_id>', VideoSubView.as_view(), name='video_sub'),
    path('video/star', VideoStarView.as_view(), name='video_star')
]
