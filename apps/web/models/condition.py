import re
from datetime import datetime
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.web.models.constants import DATE_TIME_FORMAT
from apps.web.models.update import Update

from .abstract import TimeStampModel

FULL_COINCIDENCE = 'full_coincidence'
TO_BE_IN = 'to_be_in'
CONTAINS = 'contains'
STARTS_WITH = 'starts_with'
ENDS_WITH = 'ends_with'
MATCH_REGEX = 'match_regex'
CONTAIN_AN_IMAGE = 'contain_an_image'
CONTAIN_A_FILE = 'contain_a_file'
CONTAIN_AN_AUDIO = 'contain_an_audio'
CONTAIN_A_VIDEO = 'contain_a_video'
RECEIVED_BEFORE = 'received_before'
RECEIVED_AFTER = 'received_after'
QR_CODE = 'qr_code'


RULE_CHOICES = (
    (FULL_COINCIDENCE, _('Full coincidence')),
    (TO_BE_IN, _('To be in')),
    (CONTAINS, _('Contains')),
    (STARTS_WITH, _('Starts with')),
    (ENDS_WITH, _('Ends with')),
    (MATCH_REGEX, _('Match regex')),
    (CONTAIN_AN_IMAGE, _('Contain an image')),
    (CONTAIN_A_FILE, _('Contain a file')),
    (CONTAIN_AN_AUDIO, _('Contain a audio')),
    (CONTAIN_A_VIDEO, _('Contain a video')),
    (RECEIVED_BEFORE, _('Received before')),
    (RECEIVED_AFTER, _('Received after')),
    (QR_CODE, _('QR code')),
)

ANY_MESSAGE = 'any_message'
MESSAGE_TEXT = 'message_text'
CALLBACK_MESSAGE_TEXT = 'callback_message_text'
CALLBACK_DATA = 'callback data'

FIELD_CHOICES = (
    (ANY_MESSAGE, _('Any message')),
    (MESSAGE_TEXT, _('Message text')),
    (CALLBACK_MESSAGE_TEXT, _('Callback message text')),
    (CALLBACK_DATA, _('Callback command')),
)


class Condition(TimeStampModel):
    value = models.CharField(
        verbose_name='Answer or pattern',
        max_length=1000,
    )
    rule = models.CharField(
        verbose_name='Pattern',
        max_length=255,
        choices=RULE_CHOICES,
        default=FULL_COINCIDENCE,
    )
    matched_field = models.CharField(
        verbose_name='Matched field',
        max_length=255,
        choices=FIELD_CHOICES,
        default=ANY_MESSAGE,
    )
    handler = models.ForeignKey(
        to='Handler',
        verbose_name='Attached to handler',
        related_name='conditions',
        on_delete=models.CASCADE,
    )


    def __str__(self):
        return f'{self.rule}'

    def is_match_to_rule(self, update: Update, msg=''):
        """Check if update object match to the specified rule"""

        cb = update.callback_query
        mg = update.message

        if self.matched_field == ANY_MESSAGE:
            msg = update.get_message.text
        elif self.matched_field == MESSAGE_TEXT and mg:
            msg = update.message.text
        elif self.matched_field == CALLBACK_MESSAGE_TEXT and cb:
            msg = update.callback_query.message.text
        elif self.matched_field == CALLBACK_DATA and cb:
            msg = update.callback_query.data

        msg = msg or ''

        msg_text = msg.strip().lower()
        value = self.value.lower()

        if self.rule == FULL_COINCIDENCE or self.rule == QR_CODE:
            return msg_text == value
        elif self.rule == TO_BE_IN:
            return msg_text in value
        elif self.rule == CONTAINS:
            return self.value in msg_text
        elif self.rule == STARTS_WITH:
            return msg_text.startswith(value)
        elif self.rule == ENDS_WITH:
            return msg_text.endswith(value)
        elif self.rule == MATCH_REGEX:
            return bool(re.match(value, msg_text))
        elif self.rule == CONTAIN_AN_IMAGE:
            return update.get_message.photos.count()
        elif self.rule in [RECEIVED_AFTER, RECEIVED_BEFORE]:
            try:
                dt = datetime.strptime(value, DATE_TIME_FORMAT)
            except ValueError:
                return False

            if self.rule == RECEIVED_BEFORE:
                return update.modified < dt
            elif self.rule == RECEIVED_AFTER:
                return update.modified > dt
