from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from .models import Post, User
from .permissions import IsPostAuthorOrReadOnly, IsSameUser
from .serializers import (
    PostCreateSerializer,
    PostViewSerializer,
    UserProfileSerializer,
    UserSerializer,
)


# User views
class UserList(ListCreateAPIView):
    """
    List all users, or create a new user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserProfileSerializer  # return elaborate details while creating
        return UserSerializer


class UserProfile(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, or modify a user's profile.
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSameUser]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


import pyrebase
from django.contrib.auth.models import timezone

from backend.settings import FIREBASE_CONFIG

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
storage = firebase.storage()


def upload_to(instance, filename):
    now = timezone.now()
    milliseconds = now.microsecond // 1000
    post_storagename = f"posts/{instance.request.user}/{now:%Y%m%d%H%M%S}{milliseconds}{filename}"
    storage.child(post_storagename).put(instance.request.FILES["uploadImage"])
    url = storage.child(post_storagename).get_url(None)
    return url


# Post views
class PostList(ListCreateAPIView):
    """
    List all posts, or create a new post.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCreateSerializer
        return PostViewSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned posts to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Post.objects.all()
        username = self.request.query_params.get("username", None)
        if username is not None:
            queryset = queryset.filter(user__username=username)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="username",
                location=OpenApiParameter.QUERY,
                description="Filter posts by username",
                required=False,
                type=str,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            image=upload_to(self, self.request.FILES.get("uploadImage")),
        )


class PostDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post instance.
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsPostAuthorOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return PostCreateSerializer
        return PostViewSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.image:
            instance.image.delete()
        instance.delete()
