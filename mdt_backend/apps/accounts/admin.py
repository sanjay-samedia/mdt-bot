from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models import User, BotUser


admin.site.register(User, UserAdmin)

admin.site.register(BotUser)