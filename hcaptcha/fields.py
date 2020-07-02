import json
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import build_opener, Request, ProxyHandler

from django import forms
from django.utils.translation import ugettext_lazy as _

from hcaptcha.settings import DEFAULT_CONFIG, PROXIES, SECRET, TIMEOUT, VERIFY_URL
from hcaptcha.widgets import hCaptchaWidget


class hCaptchaField(forms.Field):
    widget = hCaptchaWidget
    default_error_messages = {
        'error_hcaptcha': _('hCaptcha could not be verified.'),
        'invalid_hcaptcha': _('hCaptcha could not be verified.'),
        'required': _('Please prove you are a human.'),
    }

    def __init__(self, required=True, **config):
        widget_settings = DEFAULT_CONFIG.copy()
        widget_settings.update(config)
        widget_url_settings = {}
        for prop in filter(lambda p: p in widget_settings, ('onload', 'render', 'hl')):
            widget_url_settings[prop] = widget_settings[prop]
            del widget_settings[prop]
        self.widget_settings = widget_settings

        super().__init__(label='', help_text='', required=required)

        self.widget.extra_url = widget_url_settings

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        for key, value in self.widget_settings.items():
            attrs['data-%s' % key] = value
        return attrs

    def validate(self, value):
        super().validate(value)
        opener = build_opener(ProxyHandler(PROXIES))
        post_data = urlencode({
            'secret': SECRET,
            'response': value,
        }).encode()
        request = Request(VERIFY_URL, post_data)
        try:
            response = opener.open(request, timeout=TIMEOUT)
        except HTTPError:
            raise forms.ValidationError(self.error_messages['error_hcaptcha'], code='error_hcaptcha')

        response_data = json.loads(response.read().decode("utf-8"))

        if not response_data.get('success'):
            raise forms.ValidationError(self.error_messages['invalid_hcaptcha'], code='invalid_hcaptcha')
