from behave.runner import Context
from hoare.fixures import make_request_dispatcher, make_request_builder


def use_connect_request_dispatcher(context: Context):
    """
    Provides a connect request provider into the behave Context object.

    :param context: Context
    :return: None
    """
    context.connect = make_request_dispatcher()
    context.request = None


def use_connect_request_builder(context: Context):
    """
    Provides a connect request builder into the behave Context object.

    :param context: Context
    :return: None
    """
    context.builder = make_request_builder()
