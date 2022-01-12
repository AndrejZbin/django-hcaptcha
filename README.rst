===============
Django hCaptcha
===============

Django hCaptcha provides a simple way to protect your django forms using `hCaptcha <https://www.hcaptcha.com/>`_.

Configuration
-------------

Add "hcaptcha" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'hcaptcha',
    ]

For development purposes no further configuration is required. By default, django-hCaptcha will use dummy keys.

For production, you'll need to obtain your hCaptcha site key and secret key and add them to you settings::

    HCAPTCHA_SITEKEY = '<your sitekey>'
    HCAPTCHA_SECRET = '<your secret key>'


You can also configure your hCaptcha widget globally (`see all options <https://docs.hcaptcha.com/configuration>`_)::

    HCAPTCHA_DEFAULT_CONFIG = {
        'onload': 'name_of_js_function',
        'render': 'explicit',
        'theme': 'dark',  # do not use data- prefix
        'size': 'compact',  # do not use data- prefix
        ...
    }

If you need to, you can also override default hcaptcha endpoints::


    HCAPTCHA_JS_API_URL = 'https://hcaptcha.com/1/api.js'
    HCAPTCHA_VERIFY_URL = 'https://hcaptcha.com/siteverify'

Use proxies::

     HCAPTCHA_PROXIES = {
        'http': 'http://127.0.0.1:8000',
     }

Change default verification timeout::

    HCAPTCHA_TIMEOUT = 5



Usage
-----------

Simply add hCaptchaField to your forms::

    from hcaptcha.fields import hCaptchaField

    class Forms(forms.Form):
        ....
        hcaptcha = hCaptchaField()
        ....

In your template, if you need to, you can then use `{{ form.hcaptcha }}` to access the field. 

You can override default config by passing additional arguments::

    class Forms(forms.Form):
        ....
        hcaptcha = hCaptchaField(theme='dark', size='compact')
        ....


How it Works
------------------

When a form is submitted by a user, hCaptcha's JavaScript will send two POST parameters to your backend, `g-captcha-resposne` and `h-captcha-response`. These will be received by your app and will be used to complete the `hcaptcha` form field in your backend code.

When your app receives these two values, the following will happen:
 
 - Your backend will send these values to the hCaptcha servers
 - Their servers will indicate whether the values in the fields are correct
 - If so, your `hcaptcha` form field will validate correctly
 
Unit Tests
--------------
You will need to disable the hCaptcha field in your unit tests, since your tests obviously cannot complete the hCaptcha successfully. One way to do so might be something like:

.. code-block:: python

    from unittest.mock import MagicMock, patch

    from django.test import TestCase

    @patch("hcaptcha.fields.hCaptchaField.validate", return_value=True)
    class ContactTest(TestCase):
        test_msg = {
            "name": "pandora",
            "message": "xyz",
            "hcaptcha": "xxx",  # Any truthy value is fine
        }

        def test_something(self, mock: MagicMock) -> None:
            response = self.client.post("/contact/", self.test_msg)
            self.assertEqual(response.status_code, HTTP_302_FOUND)
