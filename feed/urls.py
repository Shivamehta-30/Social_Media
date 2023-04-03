from django.urls import path
from .views import *
urlpatterns = [
    path("new/", VideoCreateView.as_view(), name="new"),
    path("/", VideoListView.as_view(), name="view"),
    path("update/<int:pk>", VideoUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", VideoDeleteView.as_view(), name="delete")
]
