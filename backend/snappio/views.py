from rest_framework.generics import (
    ListAPIView,
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


class UserPosts(ListAPIView):
    """
    List all posts of a user.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


# Post views
class PostList(ListCreateAPIView):
    """
    List all posts, or create a new post.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Post.objects.all()

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
