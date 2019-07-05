from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    device_uid = models.CharField(
        null=True,
        blank=True,
        verbose_name="Telegram user's id",
        max_length=255,
    )
    is_bot = models.BooleanField(verbose_name='User is a bot', default=False)
    current_session = models.ForeignKey(
        to='Session',
        related_name='sessions',
        verbose_name="User's current session",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    language_code = models.CharField(
        max_length=10,
        verbose_name='Language code',
        help_text='Language code from user messages got for the first time',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.username
