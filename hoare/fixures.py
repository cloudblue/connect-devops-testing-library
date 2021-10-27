from typing import Optional
from hoare.request import Dispatcher, Builder
import os

__CONNECT_API_KEY = 'CONNECT_API_KEY'
__CONNECT_API_URL = 'CONNECT_API_URL'


def __get_credentials_from_env(api_key: Optional[str] = None, api_url: Optional[str] = None) -> dict:
    """
    Retrieve credentials from environment.

    :param api_key: str
    :param api_url: str
    :return: dict
    """
    if api_key is None:
        api_key = os.getenv(key=__CONNECT_API_KEY, default='unavailable')

    if api_url is None:
        api_url = os.getenv(key=__CONNECT_API_URL, default='unavailable')

    return {'api_key': api_key, 'api_url': api_url}


def make_request_dispatcher(api_key: Optional[str] = None, api_url: Optional[str] = None) -> Dispatcher:
    """
    Initializes a Dispatcher service.

    The ConnectClient is initialized using the environment variables:
    - CONNECT_API_KEY
    - CONNECT_API_URL

    :return: Dispatcher
    """
    return Dispatcher.init(**__get_credentials_from_env(api_key, api_url))


def make_request_builder(path: Optional[str] = None) -> Builder:
    """
    Provides a Connect Request Builder

    :return: Builder
    """
    return Builder() if path is None else Builder.from_file(path)
