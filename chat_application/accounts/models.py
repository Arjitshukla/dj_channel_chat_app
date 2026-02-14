from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
        blank=True
    )

    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username
