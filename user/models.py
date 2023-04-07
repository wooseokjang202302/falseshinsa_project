from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"

    email = models.CharField(max_length=256, default='')
