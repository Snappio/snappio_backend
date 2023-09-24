from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Post, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"required": True},
            "email": {"write_only": True},
        }

        fields = ("id", "username", "email", "name", "password")

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            name=validated_data["name"],
            username=validated_data["username"],
        )
        # identify password field to be set as hashed password
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserProfileSerializer(UserSerializer):
    """
    Return user profile with posts and additional details.
    """

    # add explicit reverse relationship to posts
    posts = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Post.objects.all(),
        required=False,  # required=False is required for POST requests
    )

    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}}
        fields = ("id", "username", "email", "name", "password", "posts")


class PostCreateSerializer(ModelSerializer):
    # save the user who created the post, passed in `preform_create` method
    # of PostList view, not used to update model
    user = serializers.ReadOnlyField(source="user.username")
    name = serializers.ReadOnlyField(source="user.name")
    uploadImage = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = [
            "id",
            "name",
            "user",
            "content",
            "timestamp",
            "image",
            "uploadImage",
        ]


class PostViewSerializer(ModelSerializer):
    # save the user who created the post, passed in `preform_create` method
    # of PostList view, not used to update model
    user = serializers.ReadOnlyField(source="user.username")
    name = serializers.ReadOnlyField(source="user.name")

    class Meta:
        model = Post
        fields = "__all__"
