import pytest

from hcaptcha_field import hCaptchaWidget, hcaptcha_settings


@pytest.fixture
def js_api_url():
    return hcaptcha_settings.JS_API_URL


@pytest.fixture
def sitekey():
    return hcaptcha_settings.SITEKEY


def test_value_from_datadict(js_api_url, sitekey):
    # Value submitted in POST data
    widget = hCaptchaWidget(js_api_url=js_api_url, sitekey=sitekey)
    data = {'h-captcha-response': 'OK'}
    value_from_datadict = widget.value_from_datadict(data, None, 'captcha')
    assert value_from_datadict == 'OK'

    # Value omitted from POST data
    widget = hCaptchaWidget(js_api_url=js_api_url, sitekey=sitekey)
    data = {}
    value_from_datadict = widget.value_from_datadict(data, None, 'captcha')
    assert value_from_datadict is None


def test_get_context_simple(js_api_url, sitekey):
    # Without extra CSS class
    widget = hCaptchaWidget(js_api_url=js_api_url, sitekey=sitekey)
    widget_context = widget.get_context('captcha', None, {})
    assert 'js_api_url' in widget_context
    assert widget_context['js_api_url'] == js_api_url
    widget_attrs = widget_context['widget']['attrs']
    assert 'class' in widget_attrs
    assert widget_attrs['class'] == 'h-captcha'
    assert 'data-sitekey' in widget_attrs
    assert widget_attrs['data-sitekey'] == sitekey


def test_get_context_extra_css_class(js_api_url, sitekey):
    # With extra CSS class
    attrs = {'class': 'captcha-field'}
    widget = hCaptchaWidget(js_api_url=js_api_url, sitekey=sitekey, attrs=attrs)
    widget_context = widget.get_context('captcha', None, {})
    assert 'js_api_url' in widget_context
    assert widget_context['js_api_url'] == js_api_url
    widget_attrs = widget_context['widget']['attrs']
    assert 'class' in widget_attrs
    assert widget_attrs['class'] == 'captcha-field h-captcha'
    assert 'data-sitekey' in widget_attrs
    assert widget_attrs['data-sitekey'] == sitekey
