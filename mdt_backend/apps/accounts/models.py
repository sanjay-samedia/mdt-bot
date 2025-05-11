from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserType:
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    USER = "USER"

    @staticmethod
    def choices():
        return (
            (UserType.ADMIN, UserType.ADMIN),
            (UserType.MANAGER, UserType.MANAGER),
            (UserType.USER, UserType.USER),
        )
    

class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return '#{} {}'.format(self.id, self.email)

    def get_full_name(self):
        first_name = self.first_name
        last_name = self.last_name
        if first_name and last_name:
            return first_name + ' ' + last_name
        else:
            return first_name or last_name
        

class BotUser(models.Model):
    user_type = models.CharField(max_length=12, choices=UserType.choices(), 
                                 default=UserType.USER)
    display_name = models.CharField(max_length=60, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(get_user_model(), related_name="%(app_label)s_%(class)s", on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.display_name)

    def _get_display_name(self, user):
        if user.first_name and user.last_name:
            display_name = '{} {}'.format(user.first_name, user.last_name)
        elif user.first_name or user.last_name:
            display_name = user.first_name or user.last_name
        else:
            display_name = user.email
        return display_name

    def set_display_name(self):
        self.display_name = self._get_display_name(self.user)
        
    def validate_unique_email(self):
        qs = BotUser.objects.exclude(id=self.id)
        qs = qs.filter(user__email__iexact=self.user.email)
        assert qs.count() == 0, 'Email already exists.'

    def save(self, *args, **kwargs):
        self.set_display_name()
        self.validate_unique_email()
        super().save(*args, **kwargs)