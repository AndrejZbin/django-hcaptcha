# Django hCaptcha Field

Django hCaptcha Field provides a simple way to protect your django forms using
[hCaptcha](https://www.hcaptcha.com/).

## Installation
1. Install using pip:

    ```shell
    $ pip install django-hcaptcha-field
    ```

2. Add to `INSTALLED_APPS`:

    ```python
    INSTALLED_APPS = [
        # ...
        'hcaptcha_field'
    ]
    ```

## Configuration
For development purposes no further configuration is required. By default,
Django hCaptcha Field will use
[test keys](https://docs.hcaptcha.com/#integration-testing-test-keys).

For production, you'll need to obtain your hCaptcha site key and secret key and
add them to you settings:

  ```python
  HCAPTCHA_SITEKEY = '<your sitekey>'
  HCAPTCHA_SECRET = '<your secret key>'
  ```

You can also configure your hCaptcha widget globally
([see all options](https://docs.hcaptcha.com/configuration)):

  ```python
  HCAPTCHA_DEFAULT_CONFIG = {
      'onload': 'name_of_js_function',
      'render': 'explicit',
      'theme': 'dark',  # do not use data- prefix
      'size': 'compact',  # do not use data- prefix
      ...
  }
  ```

If you need to, you can also override default hCaptcha endpoints:

  ```python
  HCAPTCHA_JS_API_URL = 'https://hcaptcha.com/1/api.js'
  HCAPTCHA_VERIFY_URL = 'https://hcaptcha.com/siteverify'
  ```

Use proxies:

  ```python
  HCAPTCHA_PROXIES = {
     'http': 'http://127.0.0.1:8000',
  }
  ```

Change default verification timeout:

  ```python
  HCAPTCHA_TIMEOUT = 5
  ```

## Usage
Simply add hCaptchaField to your forms:

  ```python
  from hcaptcha_field.fields import hCaptchaField

  class Form(forms.Form):
      ....
      hcaptcha = hCaptchaField()
      ....
  ```

You can override default config by passing additional arguments:

  ```python
  class Form(forms.Form):
      ....
      hcaptcha = hCaptchaField(theme='dark', size='compact')
      ....
  ```
