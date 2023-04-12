from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path("new/", VideoCreateView.as_view(), name="new"),
    path("", VideoListView.as_view(), name="view"),
    path("update/<int:pk>", VideoUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", VideoDeleteView.as_view(), name="delete"),
    path('like_video/', views.like_video, name='like_video'),
    path('add_comment/<int:pk>', views.add_comment, name='add_comment')

]
