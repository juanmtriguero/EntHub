from django.contrib import admin
from main.models import Account, FollowingLog

# Enabled in production
admin.site.register(Account)

# Disabled in production
admin.site.register(FollowingLog)