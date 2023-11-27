from __future__ import annotations

from copy import deepcopy
from typing import List, Optional, Union

from faker import Faker

from connect.devops_testing.utils import find_by_id, merge, param_members, make_tier


class AssetBuilder:
    _fake = Faker(['en_US'])

    def __init__(self):
        data = {}
        self._original = deepcopy(data)
        self._data = deepcopy(data)

    def build(self) -> dict:
        asset = deepcopy(self._data)
        self._data = deepcopy(self._original)
        return asset
    
    def with_id(self, id: str) -> AssetBuilder:
        self._data = merge(self._data, self.make_id(id))
        return self

    def with_status(self, status: str) -> AssetBuilder:
        self._data = merge(self._data, self.make_status(status))
        return self
    
    def with_external_id(self, external_id: str = 'random') -> AssetBuilder:
        self._data = merge(self._data, self.make_external_id(external_id))
        return self

    def with_external_uid(self, external_uid: str = 'random') -> AssetBuilder:
        self._data = merge(self._data, self.make_external_uid(external_uid))
        return self
    
    def with_product(self, product_id: str, product_name: str = None, status: str = 'published') -> AssetBuilder:
        self._data = merge(self._data, self.make_product(product_id, product_name, status))
        return self

    def with_marketplace(self, marketplace_id: str, marketplace_name: str = None) -> AssetBuilder:
        self._data = merge(self._data, self.make_marketplace(marketplace_id, marketplace_name))
        return self

    def with_contract(self, contract_id: str, contract_type: str, contract_name: str = '') -> AssetBuilder:
        self._data = merge(self._data, {'contract': {
            'id': contract_id,
            'type': contract_type,
            'name': contract_name,
        }})
        return self
    
    def with_connection(
            self,
            connection_id: str,
            connection_type: str,
            provider: Optional[dict] = None,
            vendor: Optional[dict] = None,
            hub: Optional[dict] = None,
    ) -> AssetBuilder:
        self._data = merge(self._data, self.make_connection(connection_id, connection_type, provider, vendor, hub))
        return self
    
    def with_connection_provider(self, provider_id: str, provider_name: Optional[str] = None) -> AssetBuilder:
        self._data = merge(self._data, self.make_connection_provider(provider_id, provider_name))
        return self

    def with_connection_vendor(self, vendor_id: str, vendor_name: Optional[str] = None) -> AssetBuilder:
        self._data = merge(self._data, self.make_connection_vendor(vendor_id, vendor_name))
        return self

    def with_connection_hub(self, hub_id: str, hub_name: Optional[str] = None) -> AssetBuilder:
        self._data = merge(self._data, self.make_connection_hub(hub_id, hub_name))
        return self
    
    def with_items(self, items: List[dict]) -> AssetBuilder:
        for item in items:
            self.with_item(**item)
        return self

    def with_item(
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
    ) -> AssetBuilder:
        item = find_by_id(self._data.get('items', []), item_id)
        if item is None:
            item = {'id': item_id}
            self._data = merge(self._data, {'items': [item]})

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
        self.with_item_params(item_id, [] if params is None else params)
        return self

    def with_item_params(self, item_id: str, params: List[dict]) -> AssetBuilder:
        for param in params:
            self.with_item_param(**{'item_id': item_id, **param})
        return self

    def with_item_param(
        self,
        item_id: str,
        param_id: str,
        value: str = '',
        value_type: str = 'text',
    ) -> AssetBuilder:
        item = find_by_id(self._data.get('items', []), item_id)
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
    
    def with_params(self, params: List[dict]) -> AssetBuilder:
        for param in params:
            self.with_param(**param)
        return self

    def with_param(
        self,
        param_id: str,
        value: Optional[Union[str, dict, list]] = None,
        value_error: Optional[str] = None,
        value_type: str = 'text',
    ) -> AssetBuilder:
        param = find_by_id(self._data.get('params', []), param_id)

        if param is None:
            param = {
                'id': param_id,
                'name': param_id,
                'title': f'Asset parameter {param_id}',
                'description': f'Asset parameter description of {param_id}',
                'type': value_type,
            }
            self._data = merge(self._data, {'params': [param]})

        members = param_members(param, value, value_error)
        param.update({k: v for k, v in members.items() if v is not None})
        return self
    
    def with_configuration_params(self, params: List[dict]) -> AssetBuilder:
        for param in params:
            self.with_configuration_param(**param)
        return self

    def with_configuration_param(
            self,
            param_id: str,
            value: Optional[Union[str, dict, list]] = None,
            value_error: Optional[str] = None,
            value_type: str = 'text',
    ) -> AssetBuilder:
        param = find_by_id(self._data.get('configuration', {}).get('params', []), param_id)

        if param is None:
            param = {
                'id': param_id,
                'name': param_id,
                'title': f'Asset configuration parameter {param_id}',
                'description': f'Asset parameter configuration description of {param_id}',
                'type': value_type,
            }
            self._data = merge(self._data, {'configuration': {'params': [param]}})

        members = param_members(param, value, value_error)
        param.update({k: v for k, v in members.items() if v is not None})
        return self
    
    def with_tier(self, tier_name: str, tier: Union[str, dict]) -> AssetBuilder:
        if isinstance(tier, str):
            self._data.get('tiers', {}).get(tier_name, {}).clear()
        self._data = merge(self._data, self.make_tier(tier_name, tier))
        return self

    def with_tier_customer(self, customer_id: Union[str, dict]) -> AssetBuilder:
        return self.with_tier('customer', customer_id)

    def with_tier_tier1(self, tier1_id: Union[str, dict]) -> AssetBuilder:
        return self.with_tier('tier1', tier1_id)

    def with_tier_tier2(self, tier2_id: Union[str, dict]) -> AssetBuilder:
        return self.with_tier('tier2', tier2_id)

    @classmethod
    def make_id(cls, id: str) -> dict:
        return {'id': id}

    @classmethod
    def make_status(cls, status: str) -> dict:
        return {'status': status}
    
    @classmethod
    def make_external_id(cls, external_id: str) -> dict:
        external_id = f"{cls._fake.pyint(1000000, 9999999)}" if external_id == 'random' else external_id
        return {'external_id': external_id}

    @classmethod
    def make_external_uid(cls, external_uid: str) -> dict:
        external_uid = f"{cls._fake.uuid4()}" if external_uid == 'random' else external_uid
        return {'external_uid': external_uid}
        
    @classmethod
    def make_product(cls, product_id: str, product_name: str, status: str) -> dict:
        product = {
            'id': product_id,
            'status': status,
        }
        if product_name:
            product.update({'name': product_name})
        return {'product': product}
        
    @classmethod
    def make_marketplace(cls, marketplace_id: str, marketplace_name: str) -> dict:
        marketplace = {'id': marketplace_id}
        if marketplace_name:
            marketplace.update({'name': marketplace_name})
        return {'marketplace': marketplace}
        
    @classmethod
    def make_connection(cls,
        connection_id: str,
        connection_type: str,
        provider: Optional[dict] = None,
        vendor: Optional[dict] = None,
        hub: Optional[dict] = None,
    ) -> dict:
        connection = {
            'id': connection_id,
            'type': connection_type,
        }
        
        if provider is not None:
            connection.update({'provider': {
                'id': provider.get('id'),
                'name': provider.get('name'),
            }})
        
        if vendor is not None:
            connection.update({'vendor': {
                'id': vendor.get('id'),
                'name': vendor.get('name'),
            }})
        
        if hub is not None:
            connection.update({'hub': {
                'id': hub.get('id'),
                'name': hub.get('name'),
            }})
        
        return {'connection': connection}
        
    @classmethod
    def make_connection_provider(cls, provider_id: str, provider_name: str) -> dict:
        connection = {'provider': {
            'id': provider_id,
            'name': provider_name,
        }}
        return {'connection': connection}
        
    @classmethod
    def make_connection_vendor(cls, vendor_id: str, vendor_name: str) -> dict:
        connection = {'vendor': {
            'id': vendor_id,
            'name': vendor_name,
        }}
        return {'connection': connection}
        
    @classmethod
    def make_connection_hub(cls, hub_id: str, hub_name: str) -> dict:
        connection = {'hub': {
            'id': hub_id,
            'name': hub_name,
        }}
        return {'connection': connection}
        
    @classmethod
    def make_tier(cls, tier_name: str, tier: Union[str, dict]) -> dict:
        if isinstance(tier, str):
            tier = make_tier(tier_name) if tier == 'random' else {'id': tier}
        return {'tiers': {tier_name: tier}}
