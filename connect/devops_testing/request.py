from __future__ import annotations

from abc import abstractmethod
from copy import deepcopy
from typing import Optional

from connect.client import ConnectClient
from connect.devops_testing.utils import find_by_id, merge, request_model, request_parameters

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
        "tiers": {
            "customer": {
                "id": "TA-0000-0000-0000",
                "external_id": "00000",
                "name": "Customer Name",
                "external_uid": "00000000-0000-0000-0000-000000000000",
                "contact_info": {
                    "address_line1": "Address Line 1",
                    "address_line2": "Address Line 2",
                    "country": "US",
                    "state": "California",
                    "city": "Irvine",
                    "postal_code": "00000",
                    "contact": {
                        "first_name": "First",
                        "last_name": "Last",
                        "email": "customer@email.com",
                        "phone_number": {
                            "country_code": "+1",
                            "area_code": "555",
                            "phone_number": "8677089",
                            "extension": "",
                        },
                    },
                },
            },
            "tier1": {
                "id": "TA-0-0000-0000-0000",
                "external_id": "00000",
                "name": "Tier 1 Name",
                "external_uid": "00000000-0000-0000-0000-000000000000",
                "contact_info": {
                    "address_line1": "Address Line 1",
                    "address_line2": "Address Line 2",
                    "country": "US",
                    "state": "California",
                    "city": "Irvine",
                    "postal_code": "00000",
                    "contact": {
                        "first_name": "First",
                        "last_name": "Last",
                        "email": "tier1@email.com",
                        "phone_number": {
                            "country_code": "+1",
                            "area_code": "555",
                            "phone_number": "8677089",
                            "extension": "",
                        },
                    },
                },
            },
        },
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
        "account": {
            "id": "TA-0000-0000-0000",
        },
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


class Builder:
    def __init__(self, request: Optional[dict] = None):
        if request is None:
            request = {}

        if not isinstance(request, dict):
            raise ValueError('Request must be a dictionary.')

        self._original = deepcopy(request)
        self._request = deepcopy(request)

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

    def is_asset_request(self) -> bool:
        return 'asset' == request_model(self._request)

    def is_tier_config_request(self) -> bool:
        return 'tier-config' == request_model(self._request)

    def with_type(self, request_type: str) -> Builder:
        self._request = merge(self._request, {'type': request_type})
        return self

    def with_id(self, request_id: str) -> Builder:
        self._request = merge(self._request, {'id': request_id})
        return self

    def with_status(self, request_status) -> Builder:
        self._request = merge(self._request, {'status': request_status})
        return self

    def with_asset_id(self, asset_id: str) -> Builder:
        self._request = merge(self._request, {'asset': {'id': asset_id}})
        return self

    def with_asset_status(self, asset_status: str) -> Builder:
        self._request = merge(self._request, {'asset': {'status': asset_status}})
        return self

    def with_asset_product(self, product_id: str, status: str = 'published') -> Builder:
        self._request = merge(self._request, {'asset': {'product': {'id': product_id, 'status': status}}})
        return self

    def with_asset_marketplace(self, marketplace_id: str) -> Builder:
        self._request = merge(self._request, {'asset': {'marketplace': {'id': marketplace_id}}})
        return self

    def with_asset_param(
            self,
            param_id: str,
            value: Optional[str] = None,
            value_error: Optional[str] = None,
    ) -> Builder:
        param = find_by_id(self._request.get('asset', {}).get('params', []), param_id)

        if param is None:
            param = {
                'id': param_id,
                'name': param_id,
                'title': f'Asset parameter {param_id}',
                'description': f'Asset parameter description of {param_id}',
                'type': 'text',
                'value': '',
                'value_error': '',
            }
            self._request = merge(self._request, {'asset': {'params': [param]}})

        values = {'value': value, 'value_error': value_error}
        param.update({k: v for k, v in values.items() if v is not None})
        return self

    def with_asset_item(
            self,
            item_id: str,
            item_mpn: str,
            quantity: str = '1',
            old_quantity: str = '0',
            item_type: str = 'Reservation',
            period: str = 'Yearly',
            unit: str = 'Licenses',
            display_name: Optional[str] = None,
    ) -> Builder:
        item = find_by_id(self._request.get('asset', {}).get('items', []), item_id)
        if item is None:
            item = {'id': item_id}
            self._request = merge(self._request, {'asset': {'items': [item]}})

        item.update({
            'display_name': item_id if display_name is None else display_name,
            'mpn': item_mpn,
            'quantity': quantity,
            'old_quantity': old_quantity,
            'params': [],
            'item_type': item_type,
            'period': period,
            'type': unit,
        })
        return self

    def with_asset_item_param(self, item_id: str, param_id: str, value: str = '') -> Builder:
        item = find_by_id(self._request.get('asset', {}).get('items', []), item_id)
        if item is None:
            raise ValueError(f'Undefined item with id {item_id}')

        param = find_by_id(item.get('params', []), param_id)
        if param is None:
            param = {
                'id': param_id,
                'title': f'Parameter {param_id}',
                'description': f'Description of {param_id}',
                'type': 'text',
                'scope': 'item',
                'phase': 'configuration',
                'value': '',
            }
            item['params'].append(param)

        param.update({'value': value})
        return self

    def with_asset_configuration_param(
            self,
            param_id: str,
            value: Optional[str] = None,
            value_error: Optional[str] = None,
    ) -> Builder:
        param = find_by_id(self._request.get('asset', {}).get('configuration', {}).get('params', []), param_id)
        if param is None:
            param = {
                'id': param_id,
                'name': param_id,
                'title': f'Asset configuration parameter {param_id}',
                'description': f'Asset configuration parameter Description of {param_id}',
                'type': 'text',
            }
            self._request = merge(self._request, {'asset': {'configuration': {'params': [param]}}})

        values = {'value': value, 'value_error': value_error}
        param.update({k: v for k, v in values.items() if v is not None})
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
        return self

    def with_tier_configuration_account(self, account_id: str) -> Builder:
        self._request = merge(self._request, {'configuration': {'account': {'id': account_id}}})
        return self

    def with_tier_configuration_tier_level(self, level: int) -> Builder:
        self._request = merge(self._request, {'configuration': {'tier_level': level}})
        return self

    def with_tier_configuration_param(
            self, param_id: str,
            value: Optional[str] = None,
            value_error: Optional[str] = None,
    ) -> Builder:
        locations = [
            (
                lambda request: request.get('configuration', {}).get('params', []),
                lambda parameter: {'configuration': {'params': [parameter]}},
            ),
            (
                lambda request: request.get('params', []),
                lambda parameter: {'params': [parameter]},
            ),
        ]

        for location in locations:
            param = find_by_id(location[0](self._request), param_id)
            if param is None:
                param = {
                    'id': param_id,
                    'name': param_id,
                    'title': f'Asset parameter {param_id}',
                    'description': f'Asset parameter description of {param_id}',
                    'type': 'text',
                    'value': '',
                    'value_error': '',
                }
                self._request = merge(self._request, location[1](param))

            values = {'value': value, 'value_error': value_error}
            param.update({k: v for k, v in values.items() if v is not None})

        return self

    def build(self) -> dict:
        request = deepcopy(self._request)
        self._request = deepcopy(self._original)

        return request


class Dispatcher:
    def __init__(self, client: ConnectClient):
        self._handlers = [
            _AssetRequestRepository(client, 'asset'),
            _TierConfigRequestRepository(client, 'tier-config'),
        ]

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

    def provision_request(self, request: dict, timeout: int = 10, max_attempt: int = 20) -> dict:
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
            timeout=timeout,
            max_attempt=max_attempt,
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
