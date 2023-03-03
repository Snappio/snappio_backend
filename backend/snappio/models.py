from django.contrib.auth.models import AbstractUser, timezone
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


def upload_to(instance, filename):
    now = timezone.now()
    milliseconds = now.microsecond // 1000
    return f"posts/{instance.user}/{now:%Y%m%d%H%M%S}{milliseconds}{filename}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        _("PostImage"), upload_to=upload_to, blank=True, null=True
    )

    def __str__(self):
        return f"{self.user} posted at {self.timestamp}"
