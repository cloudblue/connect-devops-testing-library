from copy import deepcopy
from typing import List, Optional, Union

from faker import Faker


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


def make_tier(tier_name: str = 'customer') -> dict:
    _fake = Faker(['en_US'])
    tier_type = 'customer' if tier_name == 'customer' else 'reseller'

    return {
        "name": _fake.company(),
        "type": tier_type,
        "external_id": f"{_fake.pyint(1000000, 9999999)}",
        "external_uid": f"{_fake.uuid4()}",
        "contact_info": {
            "address_line1": f"{_fake.pyint(100, 999)}, {_fake.street_name()}",
            "address_line2": _fake.secondary_address(),
            "city": _fake.city(),
            "state": _fake.state(),
            "postal_code": _fake.zipcode(),
            "country": _fake.country_code(),
            "contact": {
                "first_name": _fake.first_name(),
                "last_name": _fake.last_name(),
                "email": _fake.company_email(),
                "phone_number": {
                    "country_code": f"+{_fake.pyint(1, 99)}",
                    "area_code": f"{_fake.pyint(1, 99)}",
                    "phone_number": f"{_fake.pyint(1, 999999)}",
                    "extension": f"{_fake.pyint(1, 100)}",
                },
            },
        },
    }


def param_members(
    param: dict,
    value: Optional[Union[str, dict, list]] = None,
    value_error: Optional[str] = None,
) -> dict:
    if isinstance(value, dict):
        key = 'structured_value'
        new_value = param.get(key, {})
        new_value.update(value)
    elif isinstance(value, list):
        key = 'structured_value'
        new_value = param.get(key, [])
        new_value.extend(value)
    else:
        key = 'value'
        new_value = value

    return {key: new_value, 'value_error': value_error}
