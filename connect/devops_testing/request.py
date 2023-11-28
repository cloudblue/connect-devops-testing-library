from __future__ import annotations

import json
import time
from abc import abstractmethod
from copy import deepcopy
from datetime import datetime, timedelta
from typing import List, Optional, Union

from connect.client import ConnectClient

from connect.devops_testing.builders import AssetBuilder
from connect.devops_testing.utils import find_by_id, merge, request_model, request_parameters, param_members, make_tier
from faker import Faker


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


class Builder:
    def __init__(self, request: Optional[dict] = None):
        if request is None:
            request = {}

        if not isinstance(request, dict):
            raise ValueError('Request must be a dictionary.')

        self._original = deepcopy(request)
        self._request = deepcopy(request)
        self._fake = Faker(['en_US'])

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

    def with_status(self, request_status: str) -> Builder:
        self._request = merge(self._request, {'status': request_status})
        return self

    def with_params(self, params: List[dict]) -> Builder:
        for param in params:
            self.with_param(**param)
        return self

    def with_param(
        self,
        param_id: str,
        value: Optional[Union[str, dict, list]] = None,
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

        members = param_members(param, value, value_error)
        param.update({k: v for k, v in members.items() if v is not None})
        return self

    def with_marketplace(self, marketplace_id: str, marketplace_name: str = None) -> Builder:
        marketplace = {'id': marketplace_id}
        if marketplace_name:
            marketplace.update({'name': marketplace_name})
        self._request = merge(self._request, {'marketplace': marketplace})
        return self

    def with_contract(self, contract_id: str, contract_type: str, contract_name: str = '') -> Builder:
        self._request = merge(self._request, {'contract': {
            'id': contract_id,
            'type': contract_type,
            'name': contract_name,
        }})
        return self

    def with_asset_id(self, asset_id: str) -> Builder:
        self._request = merge(self._request, {'asset': AssetBuilder.make_id(asset_id)})
        return self

    def with_asset_external_id(self, external_id: str = 'random') -> Builder:
        self._request = merge(self._request, {'asset': AssetBuilder.make_external_id(external_id)})
        return self

    def with_asset_external_uid(self, external_uid: str = 'random') -> Builder:
        self._request = merge(self._request, {'asset': AssetBuilder.make_external_uid(external_uid)})
        return self

    def with_asset_status(self, asset_status: str) -> Builder:
        self._request = merge(self._request, {'asset': AssetBuilder.make_status(asset_status)})
        return self

    def with_asset_product(self, product_id: str, product_name: str = None, status: str = 'published') -> Builder:
        self._request = merge(self._request, {'asset': AssetBuilder.make_product(product_id, product_name, status)})
        return self

    def with_asset_marketplace(self, marketplace_id: str, marketplace_name: str = None) -> Builder:
        self._request = merge(self._request, {'asset': AssetBuilder.make_marketplace(marketplace_id, marketplace_name)})
        return self.with_marketplace(marketplace_id, marketplace_name)

    def with_asset_connection(
        self,
        connection_id: str,
        connection_type: str,
        provider: Optional[dict] = None,
        vendor: Optional[dict] = None,
        hub: Optional[dict] = None,
    ) -> Builder:
        connection = AssetBuilder.make_connection(connection_id, connection_type, provider, vendor, hub)
        self._request = merge(self._request, {'asset': connection})
        return self

    def with_asset_connection_provider(self, provider_id: str, provider_name: Optional[str] = None) -> Builder:
        connection = AssetBuilder.make_connection_provider(provider_id, provider_name)
        self._request = merge(self._request, {'asset': connection})
        return self

    def with_asset_connection_vendor(self, vendor_id: str, vendor_name: Optional[str] = None) -> Builder:
        connection = AssetBuilder.make_connection_vendor(vendor_id, vendor_name)
        self._request = merge(self._request, {'asset': connection})
        return self

    def with_asset_connection_hub(self, hub_id: str, hub_name: Optional[str] = None) -> Builder:
        connection = AssetBuilder.make_connection_hub(hub_id, hub_name)
        self._request = merge(self._request, {'asset': connection})
        return self

    def with_asset_tier(self, tier_name: str, tier: Union[str, dict]) -> Builder:
        if isinstance(tier, str):
            self._request.get('asset', {}).get('tiers', {}).get(tier_name, {}).clear()
        self._request = merge(self._request, {'asset': AssetBuilder.make_tier(tier_name, tier)})
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
        value: Optional[Union[str, dict, list]] = None,
        value_error: Optional[str] = None,
        value_type: str = 'text',
    ) -> Builder:
        param = find_by_id(self._request.get('asset', {}).get('params', []), param_id)
        if param is None:
            param = {}
            self._request = merge(self._request, {'asset': {'params': [param]}})

        param.update(AssetBuilder.make_param(param_id, value, value_error, value_type))
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
            item = {}
            self._request = merge(self._request, {'asset': {'items': [item]}})
        
        item.update(AssetBuilder.make_item(
            item_id, item_mpn, quantity, old_quantity, item_type, period, unit, display_name, global_id))
        
        if params is not None:
            self.with_asset_item_params(item_id, params)
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
            param = {}
            item['params'].append(param)

        param.update(AssetBuilder.make_item_param(param_id, value, value_type))
        return self

    def with_asset_configuration_params(self, params: List[dict]) -> Builder:
        for param in params:
            self.with_asset_configuration_param(**param)
        return self

    def with_asset_configuration_param(
        self,
        param_id: str,
        value: Optional[Union[str, dict, list]] = None,
        value_error: Optional[str] = None,
        value_type: str = 'text',
    ) -> Builder:
        param = find_by_id(self._request.get('asset', {}).get('configuration', {}).get('params', []), param_id)
        if param is None:
            param = {}
            self._request = merge(self._request, {'asset': {'configuration': {'params': [param]}}})

        param.update(AssetBuilder.make_param(param_id, value, value_error, value_type))
        return self

    def with_tier_configuration_id(self, tier_configuration_id: str) -> Builder:
        self._request = merge(self._request, {'configuration': {'id': tier_configuration_id}})
        return self

    def with_tier_configuration_status(self, tier_configuration_status: str) -> Builder:
        self._request = merge(self._request, {'configuration': {'status': tier_configuration_status}})
        return self

    def with_tier_configuration_product(self, product_id: str, product_name: str = None,
                                        status: str = 'published') -> Builder:
        product = {
            'id': product_id,
            'status': status,
        }
        if product_name:
            product.update({'name': product_name})
        self._request = merge(self._request, {'configuration': {'product': product}})
        return self

    def with_tier_configuration_marketplace(self, marketplace_id: str, marketplace_name: str = None) -> Builder:
        marketplace = {'id': marketplace_id}
        if marketplace_name:
            marketplace.update({'name': marketplace_name})
        self._request = merge(self._request, {'configuration': {'marketplace': marketplace}})
        return self.with_marketplace(marketplace_id, marketplace_name)

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
        account = make_tier('reseller') if account_id == 'random' else {'id': account_id}

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
            value: Optional[Union[str, dict, list]] = None,
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

        members = param_members(param, value, value_error)
        param.update({k: v for k, v in members.items() if v is not None})

        return self.with_param(param_id, value, value_error, value_type)

    def with_tier_configuration_configuration_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict, list]] = None,
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

        members = param_members(param, value, value_error)
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

    def _schedule_request(self, request) -> dict:
        return self._get_request_handler(request).schedule(request)

    def _revoke_request(self, request) -> dict:
        return self._get_request_handler(request).revoke(request)

    def _fetch_processed_request(self, request: dict, timeout: int, max_attempt: int) -> dict:
        finder = self._get_request_handler(request)

        attempts = 0
        request = finder.find(request.get('id'))

        while request['status'] in ['pending', 'revoking'] and attempts <= max_attempt:
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
        Provisions the given request into the Connect platform and waits until
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

    def schedule_request(
            self,
            request: dict,
            timeout: Optional[int] = None,
            max_attempt: Optional[int] = None,
    ) -> dict:
        """
        Schedules the given request into the Connect platform and waits util
        the request is processed by some processor (can be manually processed)

        :param request: dict The request to be processed.
        :param timeout: int The amount of time in seconds to wait each pull.
        :param max_attempt: int The max number of pull attempts.
        :return: dict The processed request.
        """
        return self._fetch_processed_request(
            request=self._schedule_request(request),
            timeout=self._timeout if timeout is None else timeout,
            max_attempt=self._max_attempts if max_attempt is None else max_attempt,
        )

    def revoke_request(
            self,
            request: dict,
            timeout: Optional[int] = None,
            max_attempt: Optional[int] = None,
    ) -> dict:
        """
        Revokes the given request into the Connect platform and waits util
        the request is processed by some processor (can be manually processed)

        :param request: dict The request to be processed.
        :param timeout: int The amount of time in seconds to wait each pull.
        :param max_attempt: int The max number of pull attempts.
        :return: dict The processed request.
        """
        return self._fetch_processed_request(
            request=self._revoke_request(request),
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

    @abstractmethod
    def schedule(self, request: dict) -> dict:  # pragma: no cover
        """
        Schedules the request into the Connect Platform.

        :param request: dict The request to schedule.
        :return: dict The request dictionary
        """

    @abstractmethod
    def revoke(self, request: dict) -> dict:  # pragma: no cover
        """
        Revokes the request into the Connect Platform.

        :param request: dict The request to revoke.
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

    def revoke(self, request: dict) -> dict:
        shortcut = self._client.requests
        current = self.find(request.get('id'))
        if current.get('status') == 'scheduled':
            shortcut[request.get('id')].action('revoke').post(
                payload={
                    'reason': 'Revoked from E2E tests',
                },
            )
        return request

    def schedule(self, request: dict) -> dict:
        shortcut = self._client.requests
        req_current = shortcut[request.get('id')].get()
        if req_current.get('status') == 'pending':
            shortcut[request.get('id')].action('schedule').post(
                payload={
                    'planned_date': (datetime.now() + timedelta(days=10)).isoformat(),
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

    def schedule(self, request: dict) -> dict:
        """ not applicable """

    def revoke(self, request: dict) -> dict:
        """ not applicable """
