from django.contrib import admin
from main.models import Account, FollowingLog

# Disabled in production
admin.site.register(Account)
admin.site.register(FollowingLog)