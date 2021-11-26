from typing import Optional

from connect.client import ConnectClient
from connect.devops_testing.request import Builder, Dispatcher

from os import getenv

_CONNECT_API_KEY = 'CONNECT_API_KEY'
_CONNECT_API_URL = 'CONNECT_API_URL'
_CONNECT_API_PULL_TIMEOUT = 'CONNECT_API_PULL_TIMEOUT'
_CONNECT_API_PULL_MAX_ATTEMPTS = 'CONNECT_API_PULL_MAX_ATTEMPTS'


def make_request_dispatcher(
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        use_specs: bool = True,
        client: ConnectClient = None,
        timeout: Optional[int] = None,
        max_attempts: Optional[int] = None,
) -> Dispatcher:
    """
    Initializes a Dispatcher service.

    The ConnectClient is initialized using the environment variables:
    - CONNECT_API_KEY
    - CONNECT_API_URL

    The RequestDispatcher is initialized using the environment variables:
    - CONNECT_API_PULL_TIMEOUT
    - CONNECT_API_PULL_MAX_ATTEMPTS

    :return: Dispatcher
    :param api_key: Optional[str] The Connect API Key.
    :param api_url: Optional[str] The Connect API Url endpoint.
    :param client: ConnectClient Optional Connect Open API Client already
                   instantiated if this value is provided the api_key and
                   api_url will be omitted as they are not used.
    :param use_specs: bool True to initialize the Open API Specification
                      live connection
    :param timeout: int The timeout for waiting on each request refresh in seconds.
    :param max_attempts: int The max amount of time to refresh a request
    :return: Dispatcher
    """
    if client is None:
        api_key = getenv(_CONNECT_API_KEY, 'unavailable') if api_key is None else api_key
        api_url = getenv(_CONNECT_API_URL, 'unavailable') if api_url is None else api_url

        client = ConnectClient(
            api_key=api_key,
            endpoint=api_url,
            use_specs=use_specs,
        )

    timeout = getenv(_CONNECT_API_PULL_TIMEOUT, 10) if timeout is None else timeout
    max_attempts = getenv(_CONNECT_API_PULL_MAX_ATTEMPTS, 20) if max_attempts is None else max_attempts

    return Dispatcher(
        client=client,
        timeout=timeout,
        max_attempts=max_attempts,
    )


def make_request_builder(path: Optional[str] = None) -> Builder:
    """
    Provides a Connect Request Builder

    :param path: Optional[str] The optional file path to a
                 connect json request sample.
    :return: Builder
    """
    return Builder() if path is None else Builder.from_file(path)
