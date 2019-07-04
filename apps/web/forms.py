import uuid
from apps.web.models import Condition
from django import forms

from apps.web.models.condition import QR_CODE

import logging

logger = logging.getLogger(__name__)

class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = ['value', 'rule', 'matched_field', 'handler']

    def clean(self):
        value = self.cleaned_data.get('value')
        rule = self.cleaned_data.get('rule')

        if rule == QR_CODE and value == None:
            self.cleaned_data['value'] = uuid.uuid4().hex
            del self.errors['value']

        logging.warning(self.cleaned_data)
        return self.cleaned_data
