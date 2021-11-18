from connect.devops_testing import fixtures
from connect.devops_testing.request import Builder, Dispatcher


def test_should_make_successfully_the_request_builder():
    _builder = fixtures.make_request_builder()
    assert isinstance(_builder, Builder)


def test_should_make_successfully_the_request_dispatcher_with_credentials_from_env(monkeypatch):
    _dispatcher = fixtures.make_request_dispatcher(use_specs=False)
    assert isinstance(_dispatcher, Dispatcher)


def test_should_make_successfully_the_request_dispatcher_with_given_credentials(monkeypatch):
    _dispatcher = fixtures.make_request_dispatcher(api_key='sample', api_url='sample', use_specs=False)
    assert isinstance(_dispatcher, Dispatcher)
