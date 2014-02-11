from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.utils import timezone


class Note(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(blank=True)
    creation_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User)
