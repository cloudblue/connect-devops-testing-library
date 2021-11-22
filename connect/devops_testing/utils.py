from copy import deepcopy
from typing import List, Optional


def find_by_id(collection: List, element_id: str, default: Optional[dict] = None) -> Optional[dict]:
    """
    Searches for a parameter/item with the given ``id`` within the ``list``.

    :param collection: The list of parameters/items to search.
    :param element_id: The id of the parameter/item to find.
    :param default: Default value to return if item is not found.
    :return: The parameter/list, or ``default`` if it was not found.
    """
    filtered = list(filter(lambda element: element['id'] == element_id, collection))
    return filtered[0] if filtered else default


def merge(base: dict, override: dict) -> dict:
    """
    Merge two dictionaries (override into base) recursively.

    :param base: The base dictionary.
    :param override: Override dictionary to be merge into base.
    :return dict: The new dictionary.
    """
    new_base = deepcopy(base)
    for key, value in override.items():
        if key in new_base:
            if isinstance(new_base[key], dict) and isinstance(value, dict):
                new_base[key] = merge(new_base[key], value)
            elif isinstance(new_base[key], list) and isinstance(value, list):
                new_base[key] = new_base[key] + value
            else:
                new_base[key] = value
        else:
            new_base[key] = value

    return new_base


def request_model(request: dict) -> str:
    """
    Returns the request model depending on the request type.

    :param request: dict
    :return: str
    """
    filtered = list(filter(lambda model: request.get('type') in model['types'], [
        {
            'request': 'asset',
            'types': ['adjustment', 'purchase', 'change', 'suspend', 'resume', 'cancel'],
        },
        {
            'request': 'tier-config',
            'types': ['setup'],
        },
    ]))
    return filtered[0].get('request') if filtered else 'undefined'


def request_parameters(params: List[dict]) -> List[dict]:
    """
    Map the given parameters, providing only the mutable keys.

    :param params: dict The list of parameters.
    :return: dict The mapped list of parameters.
    """

    def _key(param: dict) -> str:
        return 'value' if param.get('structured_value') is None else 'structured_value'

    def _map(param: dict) -> dict:
        return {
            'id': param.get('id'),
            _key(param): param.get(_key(param), None),
            'value_error': param.get('value_error', ''),
        }

    return list(map(_map, params))
