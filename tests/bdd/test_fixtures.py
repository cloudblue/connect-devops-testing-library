from connect.devops_testing.bdd.fixtures import use_connect_request_dispatcher, use_connect_request_builder
from connect.devops_testing.request import Builder, Dispatcher


def test_should_successfully_initialize_request_builder_in_behave_context(behave_context):
    use_connect_request_builder(behave_context)

    assert isinstance(behave_context.builder, Builder)


def test_should_successfully_initialize_request_dispatcher_in_behave_context(behave_context):
    use_connect_request_dispatcher(behave_context, use_specs=False)

    assert isinstance(behave_context.connect, Dispatcher)
    assert behave_context.request == {}
