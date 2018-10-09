from django.db import models
from django.utils import timezone
from Sauti_yangu import settings


class Category(models.Model):
    """
        This is categories table, it holds all sectors the site is divided to,
        be careful when editing this as it has many relations with other tables
    """
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Notification(models.Model):
    """
        record user notification
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    def __str__(self):
        return self.text


class NotifyUser(models.Model):
    """
        Notify the user if anything they follow happens
    """
    user_notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()

    def __str__(self):
        return self.user_notification.text
