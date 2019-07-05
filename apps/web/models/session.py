from django.db import models

from .abstract import TimeStampModel


class Session(TimeStampModel):
    user = models.ForeignKey(
        to='AppUser',
        related_name='sessions',
        on_delete=models.CASCADE,
    )
    step = models.ForeignKey(
        to='Step',
        related_name='users',
        verbose_name="User's level",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user.username} | {self.created}'
