from hcaptcha_field import hcaptcha_settings


def test_default_settings():
    assert hcaptcha_settings.JS_API_URL == 'https://hcaptcha.com/1/api.js'
    assert hcaptcha_settings.VERIFY_URL == 'https://hcaptcha.com/siteverify'
    assert hcaptcha_settings.SITEKEY == '10000000-ffff-ffff-ffff-000000000001'
    assert hcaptcha_settings.SECRET == '0x0000000000000000000000000000000000000000'
    assert hcaptcha_settings.TIMEOUT == 5
    assert hcaptcha_settings.DEFAULT_CONFIG == {}
    assert hcaptcha_settings.PROXIES == {}


def test_get_setting(settings):
    settings.HCAPTCHA_SECRET = '0xdeadbeef'

    assert hcaptcha_settings.SECRET == '0xdeadbeef'  # overridden
    assert hcaptcha_settings.TIMEOUT == 5            # default
