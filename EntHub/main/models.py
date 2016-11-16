from django.db import models
from django.contrib.auth.models import User

# Account

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth = models.DateField(blank=True, null=True)
    text = models.TextField(blank=True)
    avatar = models.URLField(blank=True)

    def __unicode__(self):
        return unicode(self.user.username)