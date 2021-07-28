from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    bio = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=255, choices=UserRoles.choices,
                            default=UserRoles.USER)

    class Meta:
        ordering = ['id']
