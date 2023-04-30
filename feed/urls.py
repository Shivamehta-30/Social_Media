from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path("new/", VideoCreateView.as_view(), name="new"),
    path("", VideoListView.as_view(), name="view"),
    path("update/<int:pk>", VideoUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", VideoDeleteView.as_view(), name="delete"),
    path('add_comment/<int:pk>', views.add_comment, name='add_comment'),
    path('like_dislike_video/', like_dislike_video, name='like_dislike_video'),
    path('add_comment/<int:pk>', views.add_comment, name='add_comment'),
    path('playlist/', PlaylistListView.as_view(), name='playlist_detail'),
    path('create_playlist/', PlaylistCreateView.as_view(), name='playlist_create'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),

    path('list_playlist/', PlaylistListView.as_view(), name='playlist_list'),
    path('add_to_playlist/<int:pk>/', add_to_playlist, name='add_to_playlist'),
]
