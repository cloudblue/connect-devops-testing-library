from typing import Optional

from connect.client import ConnectClient
from connect.devops_testing.request import Builder, Dispatcher

import os

__CONNECT_API_KEY = 'CONNECT_API_KEY'
__CONNECT_API_URL = 'CONNECT_API_URL'


def make_request_dispatcher(
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        client: ConnectClient = None,
        use_specs: bool = True,
) -> Dispatcher:
    """
    Initializes a Dispatcher service.

    The ConnectClient is initialized using the environment variables:
    - CONNECT_API_KEY
    - CONNECT_API_URL

    :return: Dispatcher
    :param api_key: Optional[str] The Connect API Key.
    :param api_url: Optional[str] The Connect API Url endpoint.
    :param client: ConnectClient Optional Connect Open API Client already
                   instantiated if this value is provided the api_key and
                   api_url will be omitted as they are not used.
    :param use_specs: bool True to initialize the Open API Specification
                      live connection
    :return: Dispatcher
    """
    if client is None:
        if api_key is None:
            api_key = os.getenv(key=__CONNECT_API_KEY, default='unavailable')

        if api_url is None:
            api_url = os.getenv(key=__CONNECT_API_URL, default='unavailable')

        client = ConnectClient(
            api_key=api_key,
            endpoint=api_url,
            use_specs=use_specs,
        )

    return Dispatcher(client=client)


def make_request_builder(path: Optional[str] = None) -> Builder:
    """
    Provides a Connect Request Builder

    :param path: Optional[str] The optional file path to a
                 connect json request sample.
    :return: Builder
    """
    return Builder() if path is None else Builder.from_file(path)
