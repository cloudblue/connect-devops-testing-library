from typing import Optional

from behave.runner import Context

from connect.client import ConnectClient
from connect.devops_testing.fixtures import make_request_builder, make_request_dispatcher


def use_connect_request_dispatcher(
        context: Context,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        use_specs: bool = True,
        client: ConnectClient = None,
        timeout: int = 10,
        max_attempts: int = 20,
):
    """
    Provides a connect request provider into the behave Context object.

    :param context: Context
    :param api_key: Optional[str] The Connect API key
    :param api_url: Optional[str] The Connect API url
    :param use_specs: bool True to initialize the Open API Specification
                      live connection
    :param client: ConnectClient Optional Connect Open API Client already
                   instantiated
    :param timeout: int The timeout for waiting on each request refresh in seconds.
    :param max_attempts: int The max amount of time to refresh a request
    :return: None
    """
    context.connect = make_request_dispatcher(
        api_key=api_key,
        api_url=api_url,
        use_specs=use_specs,
        client=client,
    )
    context.timeout = timeout
    context.max_attempts = max_attempts
    context.request = {}


def use_connect_request_builder(context: Context, parameters: Optional[dict] = None):
    """
    Provides a connect request builder into the behave Context object.

    :param context: Context
    :param parameters: Optional[dict] Key-Value dictionary with the key as
                       param name and value as param id.
    :return: None
    """
    parameters = {} if parameters is None else parameters

    context.parameter = lambda name: parameters.get(name, name)
    context.builder = make_request_builder()
