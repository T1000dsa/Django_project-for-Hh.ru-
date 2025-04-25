from django.db import models
from django.contrib.auth.models import AbstractUser

from base_app.settings import DEFAULT_USER_IMAGE

# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d', 
        blank=True, 
        null=True, 
        verbose_name='Photo', 
        default=DEFAULT_USER_IMAGE)
    date_birth = models.DateField(blank=True, null=True, verbose_name='Birthday')