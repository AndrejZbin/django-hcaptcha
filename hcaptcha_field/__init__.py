import django

from .fields import hCaptchaField
from .settings import hcaptcha_settings
from .widgets import hCaptchaWidget


__all__ = ('hCaptchaField', 'hCaptchaWidget', 'hcaptcha_settings')


if django.VERSION < (3, 2):
    default_app_config = 'hcaptcha_field.apps.hCaptchaFieldConfig'
