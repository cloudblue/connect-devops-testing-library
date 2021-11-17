from unittest.mock import Mock

from behave.runner import Context

from connect.devops_testing.bdd.fixtures import use_connect_request_dispatcher, use_connect_request_builder
from connect.devops_testing.request import Builder, Dispatcher


def test_should_successfully_initialize_request_builder_in_behave_context():
    context = Context(runner=Mock())

    use_connect_request_builder(context)

    assert isinstance(context.builder, Builder)


def test_should_successfully_initialize_request_dispatcher_in_behave_context():
    context = Context(runner=Mock())

    use_connect_request_dispatcher(context, use_specs=False)

    assert isinstance(context.connect, Dispatcher)
    assert context.request is None
