from __future__ import annotations

from copy import deepcopy
from typing import Optional

from connect.client import ConnectClient
from connect.devops_testing.utils import find_by_id

import datetime
import json
import time

_request_template = {
    "id": "PR-0000-0000-0000-000",
    "type": "purchase",
    "created": datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
    "updated": datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
    "status": "pending",
    "activation_key": "",
    "reason": "",
    "note": "",
    "asset": {
        "id": "AS-0000-0000-0000",
        "status": "processing",
        "external_id": "6MDYM711YX",
        "external_uid": "2e52d249-cdb5-4222-b4cd-67db499f2699",
        "product": {
            "id": "PRD-000-000-000",
            "name": "Product Name",
            "icon": "/media/VA-000-000/PRD-000-000-000/media/PRD-000-000-000-logo_qwerty.png",
            "status": "published",
        },
        "connection": {
            "id": "CT-0000-0000-0000",
            "type": "preview",
            "provider": {
                "id": "PA-000-000",
                "name": "ACME Dispatcher",
            },
            "vendor": {
                "id": "VA-000-000",
                "name": "ACME Vendor",
            },
            "hub": {
                "id": "HB-0000-0000",
                "name": "ACME Hub",
            },
        },
        "contract": {
            "id": "CRD-00000-00000-00000",
            "name": "ACME Distribution Contract",
        },
        "marketplace": {
            "id": "MP-00000",
            "name": "Worldwide Marketplace",
            "icon": "/media/PA-000-000/marketplaces/MP-00000/icon.png",
        },
        "params": [],
        "tiers": {
            "customer": {
                "id": "TA-0000-0000-0000",
                "external_id": "88788",
                "name": "Customer Name",
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
                "external_uid": "c64ce252-2c3d-4148-bb5b-24af1584d6c8",
            },
            "tier1": {
                "id": "TA-0-0000-0000-0000",
                "external_id": "92164",
                "name": "Tier 1 Name",
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
                "external_uid": "9c0ea6a2-4b10-48c3-abee-433014c3fd73",
            },
        },
        "items": [],
        "configuration": {
            "params": [],
        },
        "events": {
            "created": {
                "at": datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
            },
            "updated": {
                "at": datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
            },
        },
    },
    "contract": {
        "id": "CRD-00000-00000-00000",
        "name": "ACME Distribution Contract",
    },
    "marketplace": {
        "id": "MP-00000",
        "name": "Worldwide Marketplace",
        "icon": "/media/PA-00-00/marketplaces/MP-00000/icon.png",
    },
    "assignee": "",
}


class Builder:
    def __init__(
            self,
            request: Optional[dict] = None,
    ):
        if request is None:
            request = _request_template

        self._request = request

    @classmethod
    def from_file(cls, path: str) -> Builder:
        with open(path) as file:
            return cls(request=json.load(file))

    def with_type(self, request_type: str) -> Builder:
        self._request['type'] = request_type
        return self

    def with_id(self, request_id: str) -> Builder:
        self._request['id'] = request_id
        return self

    def with_status(self, request_status) -> Builder:
        self._request['status'] = request_status
        return self

    def with_asset_id(self, asset_id: str) -> Builder:
        self._request['asset']['id'] = asset_id
        return self

    def with_asset_status(self, asset_status: str) -> Builder:
        self._request['asset']['status'] = asset_status
        return self

    def with_asset_product(
            self,
            product_id: str,
            name: str,
            status: str = 'published',
    ) -> Builder:
        self._request['asset']['product'].update({
            "id": product_id,
            "name": name,
            "status": status,
        })
        return self

    def with_asset_param(
            self,
            param_id: str,
            value: str = '',
            value_error: str = '',
    ) -> Builder:
        param = find_by_id(self._request['asset']['params'], param_id)
        if param is None:
            param = {
                'id': param_id,
                'title': 'Asset parameter {parameter}'.format(parameter=param_id),
                'description': 'Asset parameter description of {parameter}'.format(parameter=param_id),
                'type': 'text',
            }
            self._request['asset']['params'].append(param)
        param.update({
            "name": param_id,
            "value": value,
            "value_error": value_error,
        })
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
    ) -> Builder:
        item = find_by_id(self._request['asset']['items'], item_id)
        if item is None:
            item = {'id': item_id}
            self._request['asset']['items'].append(item)

        item.update({
            "mpn": item_mpn,
            "quantity": quantity,
            "old_quantity": old_quantity,
            "params": [],
            "item_type": item_type,
            "period": period,
            "type": unit,
        })
        return self

    def with_asset_item_param(
            self,
            item_id: str,
            param_id: str,
            value: str = '',
    ) -> Builder:
        item = find_by_id(self._request['asset']['items'], item_id)
        param = find_by_id(item['params'], param_id)
        if param is None:
            param = {
                'id': param_id,
                'title': 'Parameter {parameter}'.format(parameter=param_id),
                'description': 'Description of {parameter}'.format(parameter=param_id),
                'type': 'text',
                'constraints': {},
                'events': {},
                'scope': 'item',
                'phase': 'configuration',
            }
            item['params'].append(param)
        param.update({"value": value})
        return self

    def with_asset_configuration_param(
            self,
            param_id: str,
            value: str = '',
            value_error: str = '',
    ) -> Builder:
        param = find_by_id(self._request['asset']['configuration']['params'], param_id)
        if param is None:
            param = {
                'id': param_id,
                'title': 'Asset configuration parameter {parameter}'.format(parameter=param_id),
                'description': 'Asset configuration parameter Description of {parameter}'.format(parameter=param_id),
                'type': 'text',
            }
            self._request['asset']['configuration']['params'].append(param)
        param.update({
            "name": param_id,
            "value": value,
            "value_error": value_error,
        })
        return self

    def build(self) -> dict:
        return deepcopy(self._request)


class Dispatcher:
    def __init__(self, client: ConnectClient):
        self._client = client

    def _create_request(self, request) -> str:
        return self._client.requests.create(payload=request).get('id')

    def _fetch_processed_request(self, request_id: str, timeout: int, max_attempt: int) -> dict:
        attempts = 0
        request = self._client.requests[request_id].get()

        while request['status'] in ['pending', 'processing'] and attempts <= max_attempt:
            attempts += 1
            time.sleep(timeout)
            request = self._client.requests[request_id].get()

        return request

    def provision_request(self, request: dict, timeout: int = 10, max_attempt: int = 20) -> dict:
        return self._fetch_processed_request(
            request_id=self._create_request(request),
            timeout=timeout,
            max_attempt=max_attempt,
        )
