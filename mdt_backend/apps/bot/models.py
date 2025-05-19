from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta

from apps.accounts.models import BotUser


class BotStatus:
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    STOPPED = "STOPPED"
    FAILED = "FAILED"

    @staticmethod
    def choices():
        return (
            (BotStatus.RUNNING, BotStatus.RUNNING),
            (BotStatus.COMPLETED, BotStatus.COMPLETED),
            (BotStatus.STOPPED, BotStatus.STOPPED),
            (BotStatus.FAILED, BotStatus.FAILED),
        )


class Website(models.Model):
    url = models.URLField(max_length=256, unique=True)
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BotInstance(models.Model):
    name = models.CharField(max_length=128)
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='bot_instances')
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='bot_instances')
    requested_visits = models.PositiveIntegerField(help_text="Number of visits requested")
    visits_sent = models.PositiveIntegerField(default=0, help_text="Number of visits actually sent")
    successful_visits = models.PositiveIntegerField(default=0, help_text="Number of visits successful sent")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    min_stay_time = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)],
                                                help_text="Minimum stay time during a visit in seconds.")
    max_stay_time = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)],
                                                help_text="Maximum stay time during a visit in seconds.")
    status = models.CharField(max_length=20, choices=BotStatus.choices(), default=BotStatus.STOPPED)
    success_rate = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    task_ids = ArrayField(models.CharField(max_length=36), blank=True, default=list)  # Store Celery task IDs

    def clean(self):
        super().clean()
        if self.max_stay_time < self.min_stay_time:
            raise ValidationError("Maximum stay time cannot be less than minimum stay time.")

    def __str__(self):
        return f"{self.name} ({self.website.url})"
    
    def time_taken(self) -> str:
        """Return the duration the bot has been running (or total run time) in HH:MM:SS format."""
        end = self.end_time
        if end:
            duration = end - self.start_time
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return None

    class Meta:
        indexes = [
            models.Index(fields=['bot_user', 'status']),
        ]


class TaskLog(models.Model):
    bot_instance = models.ForeignKey(BotInstance, on_delete=models.CASCADE, related_name='task_logs')
    task_id = models.CharField(max_length=36)
    created_at = models.DateTimeField(auto_now_add=True)