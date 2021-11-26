from typing import Any, Callable, Optional

from behave import fixture
from behave.runner import Context

from connect.client import ConnectClient
from connect.devops_testing.fixtures import make_request_builder, make_request_dispatcher


@fixture
def use_connect_request_dispatcher(
        context: Context,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        use_specs: bool = True,
        client: ConnectClient = None,
        timeout: Optional[int] = None,
        max_attempts: Optional[int] = None,
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
        timeout=timeout,
        max_attempts=max_attempts,
    )

    use_connect_request_store(context)


@fixture
def use_connect_request_store(context: Context, store: Optional[dict] = None, reset: bool = False):
    """
    Provides a simple way initialize (or reset) the request store.

    :param context: Context
    :param store: dict Provide the initial state of the store.
    :param reset: bool True to reset the request store.
    :return: None
    """
    if not hasattr(context, 'request') or reset:
        context.request = {} if store is None else store


@fixture
def use_connect_request_builder(
        context: Context,
        parameters: Optional[dict] = None,
        values: Optional[dict] = None,
        shared: Optional[dict] = None,
):
    """
    Provides a connect request builder into the behave Context object.

    :param context: Context
    :param parameters: Optional[dict] Key-Value dictionary with the key as
                       param name and value as param id.
    :param values: Optional[dict] Key-Value dictionary with replaces for the values.
    :param shared: Optional[dict] Key-Value dictionary with replaces for the shared values.
    :return: None
    """

    def _make_kv_repository(dictionary: Optional[dict]) -> Callable[[str], Any]:
        dictionary = {} if dictionary is None else dictionary

        def _find_by_key(key: str) -> Any:
            return dictionary.get(key, key)

        return _find_by_key

    context.parameter = _make_kv_repository(parameters)
    context.value = _make_kv_repository(values)
    context.shared = _make_kv_repository(shared)

    context.builder = make_request_builder()
