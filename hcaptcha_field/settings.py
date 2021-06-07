from django.conf import settings


class hCaptchaSettings(object):

    DEFAULTS = {
        'JS_API_URL': 'https://hcaptcha.com/1/api.js',
        'VERIFY_URL': 'https://hcaptcha.com/siteverify',
        'SITEKEY': '10000000-ffff-ffff-ffff-000000000001',
        'SECRET': '0x0000000000000000000000000000000000000000',
        'TIMEOUT': 5,
        'DEFAULT_CONFIG': {},
        'PROXIES': {}
    }

    def __getattr__(self, attr):
        if attr not in self.DEFAULTS:
            raise AttributeError("Invalid hCaptcha setting: '%s'" % attr)

        try:
            return getattr(settings, 'HCAPTCHA_' + attr)
        except AttributeError:
            return self.DEFAULTS[attr]


hcaptcha_settings = hCaptchaSettings()
