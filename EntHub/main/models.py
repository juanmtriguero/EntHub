from django.db import models
from django.contrib.auth.models import User

# Account

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth = models.DateField(blank=True, null=True)
    text = models.TextField(blank=True)
    avatar = models.URLField(blank=True)
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True)

    def __unicode__(self):
        return str(self.user.username)

# Logs

class FollowingLog(models.Model):
    follower = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='following_logs')
    following = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='f_logs+')
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.follower) + " ha empezado a seguir a " + str(self.following)