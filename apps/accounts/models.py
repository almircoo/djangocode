from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
# Create your models here.
class Ouser(AbstractUser):
    link = models.URLField(blank=True, null=True)
    avatar = CloudinaryField(name='avatar', blank=True, null=True)

    def __str__(self):
        return self.username
