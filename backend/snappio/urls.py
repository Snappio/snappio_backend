from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # users
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
    # posts
    path("posts/", views.PostList.as_view()),
    path("posts/<int:pk>/", views.PostDetail.as_view()),
    # authentication
    path("auth/", obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
