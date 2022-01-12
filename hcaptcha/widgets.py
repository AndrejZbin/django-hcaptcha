from urllib.parse import urlencode

from django import forms

from hcaptcha.settings import JS_API_URL, SITEKEY


class hCaptchaWidget(forms.Widget):
    template_name = 'hcaptcha/forms/widgets/hcaptcha_widget.html'

    def __init__(self, *args, **kwargs):
        self.extra_url = {}
        super().__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        return data.get('h-captcha-response')

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['data-sitekey'] = SITEKEY
        return attrs

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['api_url'] = JS_API_URL
        if self.extra_url:
            context['api_url'] += '?' + urlencode(self.extra_url)
        return context
