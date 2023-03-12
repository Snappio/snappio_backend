from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from .models import Post, User
from .permissions import IsPostAuthorOrReadOnly, IsSameUser
from .serializers import PostSerializer, UserSerializer


# User views
class UserList(ListCreateAPIView):
    """
    List all users, or create a new user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user instance.
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsSameUser]
    serializer_class = UserSerializer


class UserProfile(RetrieveAPIView):
    """
    Retrieve a user's profile.
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSameUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# Post views
class PostList(ListCreateAPIView):
    """
    List all posts, or create a new post.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

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
        serializer.save(user=self.request.user)


class PostDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post instance.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsPostAuthorOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Post.objects.all()

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.image:
            instance.image.delete()
        instance.delete()
