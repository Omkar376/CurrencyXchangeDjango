from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(ugettext_lazy('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name"]

    objects = UserManager()

    profile_image = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.email