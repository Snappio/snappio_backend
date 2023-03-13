from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Post, User


class UserSerializer(ModelSerializer):
    # if required, add explicit reverse relationship
    # to posts with PrimaryKeyRelatedField

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


class PostSerializer(ModelSerializer):
    # save the user who created the post, passed in `preform_create` method
    # of PostList view, not used to update model
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Post
        fields = ["id", "user", "content", "timestamp", "image"]
