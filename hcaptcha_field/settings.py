from django.conf import settings

JS_API_URL = getattr(settings, 'HCAPTCHA_JS_API_URL', 'https://hcaptcha.com/1/api.js')
VERIFY_URL = getattr(settings, 'HCAPTCHA_VERIFY_URL', 'https://hcaptcha.com/siteverify')
SITEKEY = getattr(settings, 'HCAPTCHA_SITEKEY', '10000000-ffff-ffff-ffff-000000000001')
SECRET = getattr(settings, 'HCAPTCHA_SECRET', '0x0000000000000000000000000000000000000000')
TIMEOUT = getattr(settings, 'HCAPTCHA_TIMEOUT', 5)
DEFAULT_CONFIG = getattr(settings, 'HCAPTCHA_DEFAULT_CONFIG', {})
PROXIES = getattr(settings, 'HCAPTCHA_PROXIES', {})
