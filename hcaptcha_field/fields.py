import json
import logging
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import build_opener, Request, ProxyHandler

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from hcaptcha_field.settings import hcaptcha_settings
from hcaptcha_field.widgets import hCaptchaWidget


LOGGER = logging.getLogger('hcaptcha_field')


DATA_ATTRIBUTE_CONFIG = frozenset([
    'theme',
    'size',
    'tabindex',
    'callback',
    'expired-callback',
    'chalexpired-callback',
    'open-callback',
    'close-callback',
    'error-callback',
])


QUERY_PARAMETER_CONFIG = frozenset([
    'onload',
    'render',
    'hl',
    'recaptchacompat'
])


class hCaptchaField(forms.Field):
    widget = hCaptchaWidget
    default_error_messages = {
        'error_hcaptcha': _(
            # Translators: Error shown when an internal server error occurred.
            'Something went wrong while verifying the hCaptcha. '
            'Please try again.'
        ),
        'invalid_hcaptcha': _(
            # Translators: Error shown when visitor did not pass the hCaptcha check.
            'hCaptcha could not be verified.'
        ),
        'required': _(
            # Translators: Error shown when visitor forgot to fill in the hCaptcha.
            'Please prove you are human.'
        ),
    }

    def __init__(self, sitekey=None, **kwargs):
        """
        Initializer for `hCaptchaField` class. It determines data attributes
        for the widget class and constructs a widget if none is given. This
        constructed widget receives the URL of the JavaScript resource for the
        hCaptcha integration and the `sitekey` of the site to protect.
        """
        # Retrieve settings
        DEFAULT_CONFIG = hcaptcha_settings.DEFAULT_CONFIG
        JS_API_URL = hcaptcha_settings.JS_API_URL
        SITEKEY = hcaptcha_settings.SITEKEY

        # Determine widget data attributes
        self.widget_data_attrs = {}
        for setting in DATA_ATTRIBUTE_CONFIG:
            if setting in kwargs:
                self.widget_data_attrs[setting] = kwargs.pop(setting)
            elif setting in DEFAULT_CONFIG:
                self.widget_data_attrs[setting] = DEFAULT_CONFIG[setting]

        # If the `widget` argument is not given, instantiate `self.widget` with
        # the hCaptcha API url and the sitekey
        if 'widget' not in kwargs:
            # Determine hCaptcha API url
            query_params = {}
            for setting in QUERY_PARAMETER_CONFIG:
                if setting in kwargs:
                    query_params[setting] = kwargs.pop(setting)
                elif setting in DEFAULT_CONFIG:
                    query_params[setting] = DEFAULT_CONFIG[setting]
            if query_params:
                js_api_url = '%s?%s' % (JS_API_URL, urlencode(query_params))
            else:
                js_api_url = JS_API_URL

            # Determine hCaptcha sitekey
            self.sitekey = sitekey or SITEKEY

            # Instantiate widget
            kwargs['widget'] = self.widget(
                    js_api_url=js_api_url, sitekey=self.sitekey)

        super().__init__(**kwargs)

    def widget_attrs(self, widget):
        """
        Returns the widget attributes, including all the data attributes
        determined in the initializer.
        """
        attrs = super().widget_attrs(widget)
        for key, value in self.widget_data_attrs.items():
            attrs['data-%s' % key] = value
        return attrs

    def validate(self, value):
        """
        Validates the field by verifying the value of the hidden field
        `h-captcha-response` with their API endpoint.
        """
        super().validate(value)

        # Build request
        opener = build_opener(ProxyHandler(hcaptcha_settings.PROXIES))
        post_data = urlencode({
            'secret': hcaptcha_settings.SECRET,
            'response': value,
            'sitekey': self.sitekey,
        }).encode('utf-8')
        request = Request(hcaptcha_settings.VERIFY_URL, post_data)

        # Perform request
        try:
            response = opener.open(request, timeout=hcaptcha_settings.TIMEOUT)
        except HTTPError:
            LOGGER.exception("Failed to verify response with hCaptcha API.")
            raise ValidationError(
                self.error_messages['error_hcaptcha'],
                code='error_hcaptcha'
            )

        # Check response
        response_data = json.loads(response.read().decode('utf-8'))
        if not response_data.get('success'):
            LOGGER.error("Failed to pass hCaptcha check: %s", response_data)
            raise ValidationError(
                self.error_messages['invalid_hcaptcha'],
                code='invalid_hcaptcha'
            )
