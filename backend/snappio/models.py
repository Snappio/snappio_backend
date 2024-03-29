from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=60)
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["email", "name"]

    def __str__(self):
        return f"{self.email}"


class Post(models.Model):
    # related_name is field name in User model
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=230, blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user} posted at {self.timestamp}, image: {self.image}"
