import pytest


class ResponseMocker:
    def __init__(self, mocker):
        self.mocker = mocker

    def mock_response(self, body=None, exception=None):
        assert body is not None or exception is not None

        if body:
            response = self.mocker.Mock()
            response.read = self.mocker.Mock(return_value=body.encode('utf-8'))
            opener = self.mocker.Mock()
            opener.open = self.mocker.Mock(return_value=response)
        elif exception:
            opener = self.mocker.Mock()
            opener.open = self.mocker.Mock(side_effect=exception)

        self.mocker.patch('hcaptcha_field.fields.build_opener', return_value=opener)


@pytest.fixture
def response_mocker(mocker):
    return ResponseMocker(mocker)
