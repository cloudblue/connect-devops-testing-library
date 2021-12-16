from __future__ import annotations

from abc import abstractmethod
from copy import deepcopy
from typing import List, Optional, Union

from connect.client import ConnectClient
from connect.devops_testing.utils import find_by_id, merge, request_model, request_parameters

from faker import Faker

import json
import time

_asset_template = {
    "type": "purchase",
    "status": "pending",
    "asset": {
        "status": "processing",
        "external_id": "0000000000",
        "external_uid": "00000000-0000-0000-0000-000000000000",
        "product": {
            "id": "PRD-000-000-000",
            "status": "published",
        },
        "connection": {
            "id": "CT-0000-0000-0000",
            "type": "preview",
        },
        "params": [],
        "tiers": {},
        "items": [],
        "configuration": {
            "params": [],
        },
        "marketplace": {
            "id": "MP-00000",
        },
    },
}

_tier_config_template = {
    "type": "setup",
    "status": "pending",
    "configuration": {
        "status": "active",
        "account": {},
        "product": {
            "id": "PRD-000-000-000",
            "status": "published",
        },
        "tier_level": 1,
        "marketplace": {
            "id": "MP-00000",
        },
        "params": [],
    },
}


def _param_members(
        param: dict,
        value: Optional[Union[str, dict]] = None,
        value_error: Optional[str] = None,
) -> dict:
    if isinstance(value, dict):
        key = 'structured_value'
        new_value = param.get(key, {})
        new_value.update(value)
    else:
        key = 'value'
        new_value = value

    return {key: new_value, 'value_error': value_error}


class Builder:
    def __init__(self, request: Optional[dict] = None):
        if request is None:
            request = {}

        if not isinstance(request, dict):
            raise ValueError('Request must be a dictionary.')

        self._original = deepcopy(request)
        self._request = deepcopy(request)
        self._fake = Faker(['en_US'])

    def _make_tier(self, tier_type: str = 'customer') -> dict:
        return {
            "name": self._fake.company(),
            "type": tier_type,
            "external_id": f"{self._fake.pyint(1000000, 9999999)}",
            "external_uid": f"{self._fake.uuid4()}",
            "contact_info": {
                "address_line1": f"{self._fake.pyint(100, 999)}, {self._fake.street_name()}",
                "address_line2": self._fake.secondary_address(),
                "city": self._fake.city(),
                "state": self._fake.state(),
                "postal_code": self._fake.zipcode(),
                "country": self._fake.country_code(),
                "contact": {
                    "first_name": self._fake.first_name(),
                    "last_name": self._fake.last_name(),
                    "email": self._fake.company_email(),
                    "phone_number": {
                        "country_code": f"+{self._fake.pyint(1, 99)}",
                        "area_code": f"{self._fake.pyint(1, 99)}",
                        "phone_number": f"{self._fake.pyint(1, 999999)}",
                        "extension": f"{self._fake.pyint(1, 100)}",
                    },
                },
            },
        }

    @classmethod
    def from_file(cls, path: str) -> Builder:
        with open(path) as file:
            return cls(request=json.load(file))

    @classmethod
    def from_default_asset(cls) -> Builder:
        return cls(request=_asset_template)

    @classmethod
    def from_default_tier_config(cls) -> Builder:
        return cls(request=_tier_config_template)

    def without(self, key: str) -> Builder:
        self._request.pop(key, None)
        return self

    def request_type(self) -> str:
        return request_model(self._request)

    def is_asset_request(self) -> bool:
        return 'asset' == self.request_type()

    def is_tier_config_request(self) -> bool:
        return 'tier-config' == self.request_type()

    def with_type(self, request_type: str) -> Builder:
        self._request = merge(self._request, {'type': request_type})
        return self

    def with_id(self, request_id: str) -> Builder:
        self._request = merge(self._request, {'id': request_id})
        return self

    def with_note(self, note: str) -> Builder:
        self._request = merge(self._request, {'note': note})
        return self

    def with_reason(self, reason: str) -> Builder:
        self._request = merge(self._request, {'reason': reason})
        return self

    def with_status(self, request_status) -> Builder:
        self._request = merge(self._request, {'status': request_status})
        return self

    def with_params(self, params: List[dict]) -> Builder:
        for param in params:
            self.with_param(**param)
        return self

    def with_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict]] = None,
            value_error: Optional[str] = None,
            value_type: str = 'text',
    ) -> Builder:
        param = find_by_id(self._request.get('params', []), param_id)

        if param is None:
            param = {
                'id': param_id,
                'name': param_id,
                'title': f'Request parameter {param_id}',
                'description': f'Request parameter description of {param_id}',
                'type': value_type,
            }
            self._request = merge(self._request, {'params': [param]})

        members = _param_members(param, value, value_error)
        param.update({k: v for k, v in members.items() if v is not None})
        return self

    def with_marketplace(self, marketplace_id: str) -> Builder:
        self._request = merge(self._request, {'marketplace': {'id': marketplace_id}})
        return self

    def with_asset_id(self, asset_id: str) -> Builder:
        self._request = merge(self._request, {'asset': {'id': asset_id}})
        return self

    def with_asset_external_id(self, external_id: str = 'random') -> Builder:
        external_id = f"{self._fake.pyint(1000000, 9999999)}" if external_id == 'random' else external_id
        self._request = merge(self._request, {'asset': {'external_id': external_id}})
        return self

    def with_asset_external_uid(self, external_uid: str = 'random') -> Builder:
        external_uid = f"{self._fake.uuid4()}" if external_uid == 'random' else external_uid
        self._request = merge(self._request, {'asset': {'external_uid': external_uid}})
        return self

    def with_asset_status(self, asset_status: str) -> Builder:
        self._request = merge(self._request, {'asset': {'status': asset_status}})
        return self

    def with_asset_product(self, product_id: str, status: str = 'published') -> Builder:
        self._request = merge(self._request, {'asset': {'product': {'id': product_id, 'status': status}}})
        return self

    def with_asset_marketplace(self, marketplace_id: str) -> Builder:
        self._request = merge(self._request, {'asset': {'marketplace': {'id': marketplace_id}}})
        return self.with_marketplace(marketplace_id)

    def with_asset_connection(
            self,
            connection_id: str,
            connection_type: str,
            provider: Optional[dict] = None,
            vendor: Optional[dict] = None,
            hub: Optional[dict] = None,
    ) -> Builder:
        self._request = merge(self._request, {'asset': {'connection': {
            'id': connection_id,
            'type': connection_type,
        }}})
        if provider is not None:
            self.with_asset_connection_provider(
                provider_id=provider.get('id'),
                provider_name=provider.get('name'),
            )
        if vendor is not None:
            self.with_asset_connection_vendor(
                vendor_id=vendor.get('id'),
                vendor_name=vendor.get('name'),
            )
        if hub is not None:
            self.with_asset_connection_hub(
                hub_id=hub.get('id'),
                hub_name=hub.get('name'),
            )

        return self

    def with_asset_connection_provider(self, provider_id: str, provider_name: Optional[str] = None) -> Builder:
        self._request = merge(self._request, {'asset': {'connection': {'provider': {
            'id': provider_id,
            'name': provider_name,
        }}}})
        return self

    def with_asset_connection_vendor(self, vendor_id: str, vendor_name: Optional[str] = None) -> Builder:
        self._request = merge(self._request, {'asset': {'connection': {'vendor': {
            'id': vendor_id,
            'name': vendor_name,
        }}}})
        return self

    def with_asset_connection_hub(self, hub_id: str, hub_name: Optional[str] = None) -> Builder:
        self._request = merge(self._request, {'asset': {'connection': {'hub': {
            'id': hub_id,
            'name': hub_name,
        }}}})
        return self

    def with_asset_tier(self, tier_name: str, tier: Union[str, dict]) -> Builder:
        if isinstance(tier, str):
            self._request.get('asset', {}).get('tiers', {}).get(tier_name, {}).clear()
            tier = self._make_tier(tier_name) if tier == 'random' else {'id': tier}

        self._request = merge(self._request, {'asset': {'tiers': {tier_name: tier}}})
        return self

    def with_asset_tier_customer(self, customer_id: Union[str, dict]) -> Builder:
        return self.with_asset_tier('customer', customer_id)

    def with_asset_tier_tier1(self, tier1_id: Union[str, dict]) -> Builder:
        return self.with_asset_tier('tier1', tier1_id)

    def with_asset_tier_tier2(self, tier2_id: Union[str, dict]) -> Builder:
        return self.with_asset_tier('tier2', tier2_id)

    def with_asset_params(self, params: List[dict]) -> Builder:
        for param in params:
            self.with_asset_param(**param)
        return self

    def with_asset_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict]] = None,
            value_error: Optional[str] = None,
            value_type: str = 'text',
    ) -> Builder:
        param = find_by_id(self._request.get('asset', {}).get('params', []), param_id)

        if param is None:
            param = {
                'id': param_id,
                'name': param_id,
                'title': f'Asset parameter {param_id}',
                'description': f'Asset parameter description of {param_id}',
                'type': value_type,
            }
            self._request = merge(self._request, {'asset': {'params': [param]}})

        members = _param_members(param, value, value_error)
        param.update({k: v for k, v in members.items() if v is not None})
        return self

    def with_asset_items(self, items: List[dict]) -> Builder:
        for item in items:
            self.with_asset_item(**item)
        return self

    def with_asset_item(
            self,
            item_id: str,
            item_mpn: str,
            quantity: str = '1',
            old_quantity: Optional[str] = None,
            item_type: Optional[str] = None,
            period: Optional[str] = None,
            unit: Optional[str] = None,
            display_name: Optional[str] = None,
            global_id: Optional[str] = None,
            params: Optional[List[dict]] = None,
    ) -> Builder:
        item = find_by_id(self._request.get('asset', {}).get('items', []), item_id)
        if item is None:
            item = {'id': item_id}
            self._request = merge(self._request, {'asset': {'items': [item]}})

        members = {
            'global_id': global_id,
            'display_name': display_name,
            'mpn': item_mpn,
            'quantity': quantity,
            'old_quantity': old_quantity,
            'params': [],
            'item_type': item_type,
            'period': period,
            'type': unit,
        }

        item.update({k: v for k, v in members.items() if v is not None})
        self.with_asset_item_params(item_id, [] if params is None else params)
        return self

    def with_asset_item_params(self, item_id: str, params: List[dict]) -> Builder:
        for param in params:
            self.with_asset_item_param(**{'item_id': item_id, **param})
        return self

    def with_asset_item_param(
            self,
            item_id: str,
            param_id: str,
            value: str = '',
            value_type: str = 'text',
    ) -> Builder:
        item = find_by_id(self._request.get('asset', {}).get('items', []), item_id)
        if item is None:
            raise ValueError(f'Undefined item with id {item_id}')

        param = find_by_id(item.get('params', []), param_id)
        if param is None:
            param = {
                'id': param_id,
                'title': f'Parameter {param_id}',
                'description': f'Description of {param_id}',
                'type': value_type,
                'scope': 'item',
                'phase': 'configuration',
                'value': '',
            }
            item['params'].append(param)

        param.update({'value': value})
        return self

    def with_asset_configuration_params(self, params: List[dict]) -> Builder:
        for param in params:
            self.with_asset_configuration_param(**param)
        return self

    def with_asset_configuration_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict]] = None,
            value_error: Optional[str] = None,
            value_type: str = 'text',
    ) -> Builder:
        param = find_by_id(self._request.get('asset', {}).get('configuration', {}).get('params', []), param_id)

        if param is None:
            param = {
                'id': param_id,
                'name': param_id,
                'title': f'Asset configuration parameter {param_id}',
                'description': f'Asset parameter configuration description of {param_id}',
                'type': value_type,
            }
            self._request = merge(self._request, {'asset': {'configuration': {'params': [param]}}})

        members = _param_members(param, value, value_error)
        param.update({k: v for k, v in members.items() if v is not None})
        return self

    def with_tier_configuration_id(self, tier_configuration_id: str) -> Builder:
        self._request = merge(self._request, {'configuration': {'id': tier_configuration_id}})
        return self

    def with_tier_configuration_status(self, tier_configuration_status: str) -> Builder:
        self._request = merge(self._request, {'configuration': {'status': tier_configuration_status}})
        return self

    def with_tier_configuration_product(self, product_id: str, status: str = 'published') -> Builder:
        self._request = merge(self._request, {'configuration': {'product': {'id': product_id, 'status': status}}})
        return self

    def with_tier_configuration_marketplace(self, marketplace_id: str) -> Builder:
        self._request = merge(self._request, {'configuration': {'marketplace': {'id': marketplace_id}}})
        return self.with_marketplace(marketplace_id)

    def with_tier_configuration_connection(
            self,
            connection_id: str,
            connection_type: str,
            provider: Optional[dict] = None,
            vendor: Optional[dict] = None,
            hub: Optional[dict] = None,
    ) -> Builder:
        self._request = merge(self._request, {'configuration': {'connection': {
            'id': connection_id,
            'type': connection_type,
        }}})
        if provider is not None:
            self.with_tier_configuration_connection_provider(
                provider_id=provider.get('id'),
                provider_name=provider.get('name'),
            )
        if vendor is not None:
            self.with_tier_configuration_connection_vendor(
                vendor_id=vendor.get('id'),
                vendor_name=vendor.get('name'),
            )
        if hub is not None:
            self.with_tier_configuration_connection_hub(
                hub_id=hub.get('id'),
                hub_name=hub.get('name'),
            )
        return self

    def with_tier_configuration_connection_provider(
            self,
            provider_id: str,
            provider_name: Optional[str] = None,
    ) -> Builder:
        self._request = merge(self._request, {'configuration': {'connection': {'provider': {
            'id': provider_id,
            'name': provider_name,
        }}}})
        return self

    def with_tier_configuration_connection_vendor(self, vendor_id: str, vendor_name: Optional[str] = None) -> Builder:
        self._request = merge(self._request, {'configuration': {'connection': {'vendor': {
            'id': vendor_id,
            'name': vendor_name,
        }}}})
        return self

    def with_tier_configuration_connection_hub(self, hub_id: str, hub_name: Optional[str] = None) -> Builder:
        self._request = merge(self._request, {'configuration': {'connection': {'hub': {
            'id': hub_id,
            'name': hub_name,
        }}}})
        return self

    def with_tier_configuration_account(self, account_id: str = 'random') -> Builder:
        account = self._make_tier('reseller') if account_id == 'random' else {'id': account_id}

        self._request = merge(self._request, {'configuration': {'account': account}})
        return self

    def with_tier_configuration_tier_level(self, level: int) -> Builder:
        self._request = merge(self._request, {'configuration': {'tier_level': level}})
        return self

    def with_tier_configuration_params(self, params: List[dict]) -> Builder:
        for param in params:
            self.with_tier_configuration_param(**param)
        return self

    def with_tier_configuration_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict]] = None,
            value_error: Optional[str] = None,
            value_type: str = 'text',
    ) -> Builder:
        param = find_by_id(self._request.get('configuration', {}).get('params', []), param_id)
        if param is None:
            param = {
                'id': param_id,
                'name': param_id,
                'title': f'Configuration parameter {param_id}',
                'description': f'Configuration parameter description of {param_id}',
                'type': value_type,
            }
            self._request = merge(self._request, {'configuration': {'params': [param]}})

        members = _param_members(param, value, value_error)
        param.update({k: v for k, v in members.items() if v is not None})

        return self.with_param(param_id, value, value_error, value_type)

    def with_tier_configuration_configuration_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict]] = None,
            value_error: Optional[str] = None,
            value_type: str = 'text',
    ) -> Builder:
        param = find_by_id(
            self._request.get('configuration', {}).get('configuration', {}).get('params', []),
            param_id,
        )
        if param is None:
            param = {
                'id': param_id,
                'title': f'Configuration parameter {param_id}',
                'description': f'Configuration parameter description of {param_id}',
                'type': value_type,
            }
            self._request = merge(self._request, {'configuration': {'configuration': {'params': [param]}}})

        members = _param_members(param, value, value_error)
        param.update({k: v for k, v in members.items() if v is not None})

        return self

    def build(self) -> dict:
        request = deepcopy(self._request)
        self._request = deepcopy(self._original)

        return request


class Dispatcher:
    def __init__(self, client: ConnectClient, timeout: int = 10, max_attempts: int = 20):
        self._handlers = [
            _AssetRequestRepository(client, 'asset'),
            _TierConfigRequestRepository(client, 'tier-config'),
        ]
        self._timeout = timeout
        self._max_attempts = max_attempts

    def _get_request_handler(self, request: dict) -> Optional[_RequestRepository]:
        filtered = list(filter(lambda handler: handler.is_type_valid(request), self._handlers))
        return filtered[0] if filtered else None

    def _save_request(self, request) -> dict:
        return self._get_request_handler(request).save(request)

    def _fetch_processed_request(self, request: dict, timeout: int, max_attempt: int) -> dict:
        finder = self._get_request_handler(request)

        attempts = 0
        request = finder.find(request.get('id'))

        while request['status'] in ['pending'] and attempts <= max_attempt:
            attempts += 1
            time.sleep(timeout)
            request = finder.find(request.get('id'))

        return request

    def provision_request(
            self,
            request: dict,
            timeout: Optional[int] = None,
            max_attempt: Optional[int] = None,
    ) -> dict:
        """
        Provision the given request into the Connect platform and waits util
        the request is processed by some processor (can be manually processed)

        :param request: dict The request to be processed.
        :param timeout: int The amount of time in seconds to wait each pull.
        :param max_attempt: int The max number of pull attempts.
        :return: dict The processed request.
        """
        return self._fetch_processed_request(
            request=self._save_request(request),
            timeout=self._timeout if timeout is None else timeout,
            max_attempt=self._max_attempts if max_attempt is None else max_attempt,
        )


class _RequestRepository:
    def __init__(self, client: ConnectClient, model: str):
        self._client = client
        self._model = model

    def is_type_valid(self, request: dict) -> bool:
        return request_model(request) == self._model

    @abstractmethod
    def find(self, request_id: str) -> dict:  # pragma: no cover
        """
        Find a request by id.

        :param request_id: str The request id
        :return: dict The request dictionary
        """

    @abstractmethod
    def save(self, request: dict) -> dict:  # pragma: no cover
        """
        Save (create/update) the request into the Connect Platform.

        :param request: dict The request to create/update.
        :return: dict The request dictionary
        """


class _AssetRequestRepository(_RequestRepository):
    def find(self, request_id: str) -> dict:
        return self._client.requests[request_id].get()

    def save(self, request: dict) -> dict:
        shortcut = self._client.requests
        if request.get('id') is None:
            request = shortcut.create(
                payload=request,
            )

        else:
            current = self.find(request.get('id'))
            params = zip(
                request_parameters(current.get('asset', {}).get('params', [])),
                request_parameters(request.get('asset', {}).get('params', [])),
            )

            difference = [new for cur, new in params if cur != new]
            if len(difference) > 0:
                if current.get('status') == 'inquiring':
                    shortcut[request.get('id')].action('pend').post()

                request = shortcut[request.get('id')].update(
                    payload={
                        'asset': {'params': difference},
                    },
                )

        return request


class _TierConfigRequestRepository(_RequestRepository):
    def find(self, request_id: str) -> dict:
        return self._client.ns('tier').config_requests[request_id].get()

    def save(self, request: dict) -> dict:
        shortcut = self._client.ns('tier').config_requests
        if request.get('id') is None:
            request = shortcut.create(
                payload=request,
            )

        else:
            current = self.find(request.get('id'))
            params = zip(
                request_parameters(current.get('params', [])),
                request_parameters(request.get('params', [])),
            )

            difference = [new for cur, new in params if cur != new]
            if len(difference) > 0:
                if current.get('status') == 'inquiring':
                    shortcut[request.get('id')].action('pend').post()

                request = shortcut[request.get('id')].update(
                    payload={
                        'params': difference,
                    },
                )

        return request
