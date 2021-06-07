from django import forms


class hCaptchaWidget(forms.Widget):
    template_name = 'hcaptcha_widget.html'

    def __init__(self, *args, js_api_url, sitekey, **kwargs):
        """
        Initializer for `hCaptchaWidget` class. It expects the URL of the
        JavaScript resource for the hCaptcha integration and the `sitekey` of
        the site to protect.
        """
        super().__init__(*args, **kwargs)

        self.js_api_url = js_api_url
        self.sitekey = sitekey

    def value_from_datadict(self, data, files, name):
        """
        hCaptcha will set a hidden field with name `h-captcha-response` with a
        code that can be verified in the backend with their API endpoint.
        """
        return data.get('h-captcha-response')

    def get_context(self, name, value, attrs):
        """
        Returns template context for widget with the correct HTML element
        attributes.
        """
        context = super().get_context(name, value, attrs)

        context['js_api_url'] = self.js_api_url

        widget_attrs = context['widget']['attrs']
        if 'class' in widget_attrs:
            widget_attrs['class'] += ' h-captcha'
        else:
            widget_attrs['class'] = 'h-captcha'
        widget_attrs['data-sitekey'] = self.sitekey

        return context
