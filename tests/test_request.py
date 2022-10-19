from connect.devops_testing.request import Builder, Dispatcher

import pytest

import os

TPL_REQUEST_ASSET = '/request_asset.json'
TPL_REQUEST_TIER_CONFIG = '/request_tier_config.json'

CFG_VALUE_ERROR = 'Some value error on configuration'


def test_request_builder_should_fail_building_request_with_wrong_template_type():
    with pytest.raises(ValueError):
        Builder(request=['wrong request argument type'])


def test_request_builder_should_use_default_asset_template():
    request = (Builder()
               .from_default_asset()
               .build())

    assert 'asset' in request


def test_request_builder_should_use_default_tier_config_template():
    request = (Builder()
               .from_default_tier_config()
               .build())

    assert 'configuration' in request


def test_request_builder_should_raise_exception_on_adding_parameter_to_missing_asset_item():
    with pytest.raises(ValueError):
        (Builder()
         .with_asset_item_param('MISSING', 'PARAM_ID', 'The value'))


def test_request_builder_should_build_successfully_a_valid_asset_request():
    request = Builder()
    request.with_type('purchase')
    request.with_status('approved')
    request.with_id('PR-0000-0000-0000-100')
    request.with_asset_external_id('123456789')
    request.with_asset_external_uid('9fb50525-a4a4-41a7-ace0-dc3c73796d32')
    request.with_asset_product('PRD-000-000-100', 'disabled')
    request.with_asset_id('AS-0000-0000-1000')
    request.with_asset_status('active')
    request.with_asset_marketplace('MP-12345')
    request.with_asset_connection(
        connection_id='CT-0000-0000-0000',
        connection_type='test',
        provider={"id": "PA-800-926", "name": "IMC Gamma Team Provider"},
        vendor={"id": "VA-610-138", "name": "IMC Gamma Team Vendor"},
        hub={"id": "HB-0000-0000", "name": "None"},
    )
    request.with_asset_params([
        {'param_id': 'PARAM_ID_001', 'value': 'VALUE_001'},
        {'param_id': 'PARAM_ID_002', 'value': 'VALUE_002'},
        {'param_id': 'PARAM_ID_003', 'value': '', 'value_error': 'Some value error on asset', },
        {'param_id': 'PARAM_ID_001', 'value': 'VALUE_001_UPDATED'},
    ])
    request.with_asset_items([
        {
            'item_id': 'ITEM_ID_001',
            'item_mpn': 'ITEM_MPN_001',
            'params': [{'param_id': 'SOME_ITEM_PARAM_ID', 'value': 'ITEM_ID_001_PARAM_VALUE'}]
        },
        {
            'item_id': 'ITEM_ID_001',
            'item_mpn': 'ITEM_MPN_001_UPDATED',
        },
        {
            'item_id': 'ITEM_ID_001',
            'item_mpn': 'ITEM_MPN_001_UPDATED',
            'params': [{'param_id': 'SOME_ITEM_PARAM_ID', 'value': 'ITEM_ID_001_PARAM_VALUE_UPDATED'}]
        }
    ])
    request.with_asset_configuration_params([
        {'param_id': 'AS_CFG_ID_001', 'value': 'Cfg value', 'value_error': 'Cfg error value'},
        {'param_id': 'AS_CFG_ID_001', 'value': 'Cfg value updated', 'value_error': 'Cfg error value updated'},
        {'param_id': 'IS_A_LIST_001', 'value': [1, 2]},
        {'param_id': 'IS_A_LIST_001', 'value': [3, 4]},
    ])

    assert request.is_asset_request()

    request = request.build()

    assert request['id'] == 'PR-0000-0000-0000-100'
    assert request['type'] == 'purchase'
    assert request['status'] == 'approved'
    assert request['marketplace']['id'] == 'MP-12345'

    assert request['asset']['id'] == 'AS-0000-0000-1000'
    assert request['asset']['status'] == 'active'

    assert request['asset']['external_id'] == '123456789'
    assert request['asset']['external_uid'] == '9fb50525-a4a4-41a7-ace0-dc3c73796d32'

    assert request['asset']['marketplace']['id'] == 'MP-12345'

    assert request['asset']['connection']['id'] == 'CT-0000-0000-0000'
    assert request['asset']['connection']['type'] == 'test'
    assert request['asset']['connection']['provider']['id'] == 'PA-800-926'
    assert request['asset']['connection']['provider']['name'] == 'IMC Gamma Team Provider'
    assert request['asset']['connection']['vendor']['id'] == 'VA-610-138'
    assert request['asset']['connection']['vendor']['name'] == 'IMC Gamma Team Vendor'
    assert request['asset']['connection']['hub']['id'] == 'HB-0000-0000'
    assert request['asset']['connection']['hub']['name'] == 'None'

    assert request['asset']['product']['id'] == 'PRD-000-000-100'
    assert request['asset']['product']['status'] == 'disabled'

    assert request['asset']['params'][0]['id'] == 'PARAM_ID_001'
    assert request['asset']['params'][0]['value'] == 'VALUE_001_UPDATED'

    assert request['asset']['params'][1]['id'] == 'PARAM_ID_002'
    assert request['asset']['params'][1]['value'] == 'VALUE_002'

    assert request['asset']['params'][2]['id'] == 'PARAM_ID_003'
    assert request['asset']['params'][2]['value'] == ''
    assert request['asset']['params'][2]['value_error'] == 'Some value error on asset'

    assert request['asset']['items'][0]['id'] == 'ITEM_ID_001'
    assert request['asset']['items'][0]['mpn'] == 'ITEM_MPN_001_UPDATED'

    assert request['asset']['items'][0]['params'][0]['id'] == 'SOME_ITEM_PARAM_ID'
    assert request['asset']['items'][0]['params'][0]['value'] == 'ITEM_ID_001_PARAM_VALUE_UPDATED'

    assert request['asset']['configuration']['params'][0]['id'] == 'AS_CFG_ID_001'
    assert request['asset']['configuration']['params'][0]['value'] == 'Cfg value updated'
    assert request['asset']['configuration']['params'][0]['value_error'] == 'Cfg error value updated'

    assert request['asset']['configuration']['params'][1]['id'] == 'IS_A_LIST_001'
    assert request['asset']['configuration']['params'][1]['structured_value'] == [1, 2, 3, 4]


def test_request_builder_should_build_successfully_a_valid_tier_config_request():
    request = Builder()
    request.with_type('setup')
    request.with_status('approved')
    request.with_id('TCR-000-000-000-100')
    request.with_tier_configuration_id('TC-000-000-000')
    request.with_tier_configuration_status('active')
    request.with_tier_configuration_marketplace('MP-12345')
    request.with_tier_configuration_connection(
        connection_id='CT-0000-0000-0000',
        connection_type='test',
        provider={"id": "PA-800-926", "name": "IMC Gamma Team Provider"},
        vendor={"id": "VA-610-138", "name": "IMC Gamma Team Vendor"},
        hub={"id": "HB-0000-0000", "name": "None"},
    )
    request.with_tier_configuration_configuration_param('P_CFG_CFG_ID', 'CFG_VALUE')
    request.with_tier_configuration_configuration_param('P_CFG_CFG_ID', 'CFG_VALUE_UPDATED')
    request.with_tier_configuration_product('PRD-000-000-100', 'disabled')
    request.with_tier_configuration_account('TA-0000-0000-1000')
    request.with_tier_configuration_tier_level(2)
    request.with_tier_configuration_params([
        {'param_id': 'PARAM_ID_001', 'value': 'VALUE_001'},
        {'param_id': 'PARAM_ID_002', 'value': 'VALUE_002'},
        {'param_id': 'PARAM_ID_003', 'value': '', 'value_error': CFG_VALUE_ERROR},
        {'param_id': 'PARAM_ID_001', 'value': 'VALUE_001_UPDATED'},
    ])
    request.with_params([
        {'param_id': 'PARAM_ID_001', 'value': 'VALUE_001_UPDATED'},
    ])

    assert request.is_tier_config_request()

    request = request.build()

    assert request['id'] == 'TCR-000-000-000-100'
    assert request['type'] == 'setup'
    assert request['status'] == 'approved'
    assert request['marketplace']['id'] == 'MP-12345'

    assert request['configuration']['id'] == 'TC-000-000-000'
    assert request['configuration']['status'] == 'active'

    assert request['configuration']['marketplace']['id'] == 'MP-12345'

    assert request['configuration']['connection']['id'] == 'CT-0000-0000-0000'
    assert request['configuration']['connection']['type'] == 'test'
    assert request['configuration']['connection']['provider']['id'] == 'PA-800-926'
    assert request['configuration']['connection']['provider']['name'] == 'IMC Gamma Team Provider'
    assert request['configuration']['connection']['vendor']['id'] == 'VA-610-138'
    assert request['configuration']['connection']['vendor']['name'] == 'IMC Gamma Team Vendor'
    assert request['configuration']['connection']['hub']['id'] == 'HB-0000-0000'
    assert request['configuration']['connection']['hub']['name'] == 'None'

    assert request['configuration']['configuration']['params'][0]['id'] == 'P_CFG_CFG_ID'
    assert request['configuration']['configuration']['params'][0]['value'] == 'CFG_VALUE_UPDATED'

    assert request['configuration']['product']['id'] == 'PRD-000-000-100'
    assert request['configuration']['product']['status'] == 'disabled'

    assert request['configuration']['account']['id'] == 'TA-0000-0000-1000'

    assert request['configuration']['tier_level'] == 2

    assert len(request['configuration']['params']) == 3

    assert request['configuration']['params'][0]['id'] == 'PARAM_ID_001'
    assert request['configuration']['params'][0]['value'] == 'VALUE_001_UPDATED'

    assert request['configuration']['params'][1]['id'] == 'PARAM_ID_002'
    assert request['configuration']['params'][1]['value'] == 'VALUE_002'

    assert request['configuration']['params'][2]['id'] == 'PARAM_ID_003'
    assert request['configuration']['params'][2]['value'] == ''
    assert request['configuration']['params'][2]['value_error'] == CFG_VALUE_ERROR

    assert len(request['params']) == 3

    assert request['params'][0]['id'] == 'PARAM_ID_001'
    assert request['params'][0]['value'] == 'VALUE_001_UPDATED'

    assert request['params'][1]['id'] == 'PARAM_ID_002'
    assert request['params'][1]['value'] == 'VALUE_002'

    assert request['params'][2]['id'] == 'PARAM_ID_003'
    assert request['params'][2]['value'] == ''
    assert request['params'][2]['value_error'] == CFG_VALUE_ERROR


def test_request_builder_should_build_successfully_a_valid_tier_config_request_with_random_account_data():
    request = (Builder()
               .with_type('setup')
               .with_status('approved')
               .with_id('TCR-000-000-000-100')
               .with_tier_configuration_id('TC-000-000-000')
               .with_tier_configuration_account('random'))

    assert request.is_tier_config_request()

    request = request.build()

    assert request['id'] == 'TCR-000-000-000-100'
    assert request['type'] == 'setup'
    assert request['status'] == 'approved'

    assert 'contact_info' in request['configuration']['account']


def test_request_builder_should_build_successfully_a_valid_request_from_file_template():
    template = os.path.dirname(__file__) + TPL_REQUEST_ASSET

    request = (Builder.from_file(template)
               .build())

    assert request['id'] == 'PR-7658-9572-0778-001'
    assert request['type'] == 'purchase'
    assert request['status'] == 'pending'

    assert request['asset']['id'] == 'AS-7658-9572-0778'
    assert request['asset']['status'] == 'processing'


def test_request_dispatcher_should_create_successfully_a_asset_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + TPL_REQUEST_ASSET

    request = Builder.from_file(template)

    to_create = (request
                 .without('id')
                 .build())

    pending = request.build()

    approved = (request
                .with_status('approved')
                .with_asset_status('active')
                .build())

    connect_client = sync_client_factory([
        response_factory(value=pending),  # request.create
        response_factory(value=pending),  # request.get (first call)
        response_factory(value=approved),  # request.get (second call)
    ])

    request = (Dispatcher(client=connect_client)
               .provision_request(request=to_create, timeout=0, max_attempt=1))

    assert isinstance(request, dict)


def test_request_dispatcher_should_update_successfully_a_asset_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + TPL_REQUEST_ASSET

    request = Builder.from_file(template)

    on_server = (request
                 .with_status('inquiring')
                 .build())

    to_update = (request
                 .with_asset_param('UNIQUE_PURCHASE_ORDER_IDENTIFIER', 'SOME_VALID_VALUE')
                 .build())

    approved = (request
                .with_status('approved')
                .with_asset_status('active')
                .with_asset_param('UNIQUE_PURCHASE_ORDER_IDENTIFIER', 'SOME_VALID_VALUE')
                .build())

    connect_client = sync_client_factory([
        response_factory(value=on_server),  # request.get (to compare)
        response_factory(status=204),  # request.update (set to pending)
        response_factory(value=to_update),  # request.update (update params)
        response_factory(value=to_update),  # request.get (first call)
        response_factory(value=approved),  # request.get (second call)
    ])

    request = (Dispatcher(client=connect_client)
               .provision_request(request=to_update, timeout=0, max_attempt=1))

    assert request['asset']['params'][0]['value'] == 'SOME_VALID_VALUE'


def test_request_dispatcher_should_avoid_update_a_unchanged_asset_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + TPL_REQUEST_ASSET

    request = Builder.from_file(template)

    on_server = request.build()

    to_update = (request
                 .build())

    approved = (request
                .with_status('approved')
                .with_asset_status('active')
                .build())

    connect_client = sync_client_factory([
        response_factory(value=on_server),  # request.get (to compare)
        response_factory(value=to_update),  # request.get (first call)
        response_factory(value=approved),  # request.get (second call)
    ])

    request = (Dispatcher(client=connect_client)
               .provision_request(request=to_update, timeout=0, max_attempt=1))

    assert request['asset']['params'][0]['value'] == ''


def test_request_dispatcher_should_create_successfully_a_tier_config_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + TPL_REQUEST_TIER_CONFIG

    request = Builder.from_file(template)

    to_create = (request
                 .without('id')
                 .build())

    pending = request.build()

    approved = (request
                .with_status('approved')
                .with_tier_configuration_status('active')
                .build())

    connect_client = sync_client_factory([
        response_factory(value=pending),  # tier.config_request.create
        response_factory(value=pending),  # tier.config_request.get (first call)
        response_factory(value=approved),  # tier.config_request.get (second call)
    ])

    request = (Dispatcher(client=connect_client)
               .provision_request(request=to_create, timeout=0, max_attempt=1))

    assert isinstance(request, dict)


def test_request_dispatcher_should_update_successfully_a_tier_config_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + TPL_REQUEST_TIER_CONFIG

    request = Builder.from_file(template)

    on_server = (request
                 .with_status('inquiring')
                 .build())

    to_update = (request
                 .with_tier_configuration_param('TIER1_MPN', '111111')
                 .build())

    approved = (request
                .with_status('approved')
                .with_tier_configuration_status('active')
                .with_tier_configuration_param('TIER1_MPN', '111111')
                .build())

    connect_client = sync_client_factory([
        response_factory(value=on_server),  # tier.config_request.get (to compare)
        response_factory(status=204),  # tier.config_request.update (set to pending)
        response_factory(value=to_update),  # tier.config_request.update (update params)
        response_factory(value=to_update),  # tier.config_request.get (first call)
        response_factory(value=approved),  # tier.config_request.get (second call)
    ])

    request = (Dispatcher(client=connect_client)
               .provision_request(request=to_update, timeout=0, max_attempt=1))

    assert isinstance(request, dict)
    assert request['configuration']['params'][0]['value'] == '111111'


def test_request_dispatcher_should_avoid_update_a_unchanged_tier_config_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + TPL_REQUEST_TIER_CONFIG

    request = Builder.from_file(template)

    on_server = request.build()

    to_update = (request
                 .build())

    approved = (request
                .with_status('approved')
                .with_tier_configuration_status('active')
                .build())

    connect_client = sync_client_factory([
        response_factory(value=on_server),  # tier.config_request.get (to compare)
        response_factory(value=to_update),  # tier.config_request.get (first call)
        response_factory(value=approved),  # tier.config_request.get (second call)
    ])

    request = (Dispatcher(client=connect_client)
               .provision_request(request=to_update, timeout=0, max_attempt=1))

    assert request['configuration']['params'][0]['value'] == '000000'
