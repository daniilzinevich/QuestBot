from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.web.validators import json_field_validator

from .abstract import TimeStampModel


class Chat(TimeStampModel):
    PRIVATE = 'private'
    GROUP = 'group'
    SUPERGROUP = 'supergroup'
    CHANNEL = 'channel'

    CHOICES = (
        (PRIVATE, _('Private')),
        (GROUP, _('Group')),
        (SUPERGROUP, _('Supergroup')),
        (CHANNEL, _('Channel')),
    )

    id = models.BigIntegerField(
        primary_key=True,
        unique=True,
        help_text=_('Unique identifier for this chat.'),
    )
    type = models.CharField(
        max_length=255,
        choices=CHOICES,
        verbose_name=_('Type'),
    )
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('Title, for supergroups, channels and group chats.'),
    )
    username = models.CharField(
        verbose_name=_('Unique username'),
        max_length=255,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_('First name of the other party in a private chat'),
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_('Last name of the other party in a private chat'),
    )
    default_keyboard = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name=_('Default chat menu'),
        help_text=_('Chat menu, is used to inherit markup keyboard styles')
    )
    current_keyboard = models.TextField(
        max_length=1000,
        help_text=_('Is used to define available command from keyboard'),
        editable=False,
        null=True,
        blank=True,
    )

    # chat settings

    no_notifications = models.NullBooleanField(
        verbose_name=_('Disable notifications'),
        null=True,
        blank=False,
    )
    no_links_preview = models.NullBooleanField(
        verbose_name=_('Disable links preview'),
        null=True,
        blank=False,
    )
    template_context = models.TextField(
        verbose_name=_('Template context'),
        max_length=3000,
        null=True,
        blank=True,
        validators=[json_field_validator],
    )

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')

    def __str__(self):
        """Represent chat name"""
        return ' | '.join([str(self.id), self.username])
