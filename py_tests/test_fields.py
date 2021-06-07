import json
from http import HTTPStatus
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse

import pytest
from django.core.exceptions import ValidationError

from hcaptcha_field import hCaptchaField, hCaptchaWidget, hcaptcha_settings


def test_initialization_simple():
    """
    Tests initialization of widget without any config given or default config
    set.
    """
    field = hCaptchaField()

    assert field.widget_data_attrs == {}

    assert hasattr(field.widget, 'js_api_url')
    field.widget.js_api_url == hcaptcha_settings.JS_API_URL

    assert hasattr(field.widget, 'sitekey')
    assert field.widget.sitekey == hcaptcha_settings.SITEKEY


def test_initialization_with_config(settings):
    """
    Tests initialization of widget with some config given and some default
    config set.
    """
    # Override hCaptcha default configuration
    settings.HCAPTCHA_DEFAULT_CONFIG = {
        'size': 'compact',
        'theme': 'dark',
        'render': 'onload',
    }

    field = hCaptchaField(tabindex=5, hl='nl')

    assert field.widget_data_attrs == {
        'size': 'compact',
        'theme': 'dark',
        'tabindex': 5
    }

    assert hasattr(field.widget, 'js_api_url')
    parsed_url = urlparse(field.widget.js_api_url)
    assert ('%s://%s%s' % parsed_url[:3]) == hcaptcha_settings.JS_API_URL
    parsed_qs = parse_qs(parsed_url.query)
    assert parsed_qs == {'render': ['onload'], 'hl': ['nl']}

    assert hasattr(field.widget, 'sitekey')
    assert field.widget.sitekey == hcaptcha_settings.SITEKEY


def test_initialization_custom_widget():
    """
    Tests initialization with custom widget given.
    """
    js_api_url = 'https://api.hcaptcha.com/captcha.js'
    sitekey = '0xdeadbeef'

    widget = hCaptchaWidget(js_api_url=js_api_url, sitekey=sitekey)
    field = hCaptchaField(widget=widget)
    assert field.widget.js_api_url == js_api_url
    assert field.widget.sitekey == sitekey


def test_widget_attrs():
    js_api_url = hcaptcha_settings.JS_API_URL
    sitekey = hcaptcha_settings.SITEKEY
    widget = hCaptchaWidget(js_api_url=js_api_url, sitekey=sitekey)

    field = hCaptchaField(widget=widget, size='compact', theme='dark')
    assert field.widget_attrs(widget) == {
        'data-size': 'compact',
        'data-theme': 'dark',
    }


def test_validate_success(response_mocker):
    response_mocker.mock_response(body=json.dumps({'success': True}))

    field = hCaptchaField()
    field.validate('token')


def test_validate_invalid_token(response_mocker):
    response_mocker.mock_response(body=json.dumps({'success': False}))

    field = hCaptchaField()
    with pytest.raises(ValidationError) as exception:
        field.validate('token')
    assert exception.value.code == 'invalid_hcaptcha'


def test_validate_request_failure(response_mocker):
    http_error = HTTPError(
        hcaptcha_settings.JS_API_URL,
        HTTPStatus.INTERNAL_SERVER_ERROR.value,
        HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
        "",
        None
    )
    response_mocker.mock_response(exception=http_error)

    field = hCaptchaField()
    with pytest.raises(ValidationError) as exception:
        field.validate('token')
    assert exception.value.code == 'error_hcaptcha'
