from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, User
from .permissions import IsPostAuthorOrReadOnly, IsSameUser
from .serializers import PostSerializer, UserSerializer


# User views
class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsSameUser]
    serializer_class = UserSerializer


# Post views
class PostList(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(RetrieveUpdateDestroyAPIView):
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
