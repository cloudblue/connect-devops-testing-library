from connect.devops_testing import fixtures
from connect.devops_testing.request import Builder

import pytest

import os

TPL_REQUEST_ASSET = '/request_asset.json'
TPL_REQUEST_TIER_CONFIG = '/request_tier_config.json'


def test_request_builder_should_fail_building_request_with_wrong_template_type():
    with pytest.raises(ValueError):
        Builder(request=['wrong request argument type'])


def test_request_builder_should_use_default_asset_template():
    request = (fixtures.make_request_builder()
               .from_default_asset()
               .build())

    assert 'asset' in request


def test_request_builder_should_use_default_tier_config_template():
    request = (fixtures.make_request_builder()
               .from_default_tier_config()
               .build())

    assert 'configuration' in request


def test_request_builder_should_raise_exception_on_adding_parameter_to_missing_asset_item():
    with pytest.raises(ValueError):
        (fixtures.make_request_builder()
         .with_asset_item_param('MISSING', 'PARAM_ID', 'The value'))


def test_request_builder_should_build_successfully_a_valid_asset_request():
    request = (fixtures.make_request_builder()
               .with_type('purchase')
               .with_status('approved')
               .with_id('PR-0000-0000-0000-100')
               .with_asset_product('PRD-000-000-100', 'disabled')
               .with_asset_id('AS-0000-0000-1000')
               .with_asset_status('active')
               .with_asset_marketplace('MP-12345')
               .with_asset_param('PARAM_ID_001', 'VALUE_001')
               .with_asset_param('PARAM_ID_002', 'VALUE_002')
               .with_asset_param('PARAM_ID_003', '', 'Some value error on asset')
               .with_asset_param('PARAM_ID_001', 'VALUE_001_UPDATED')
               .with_asset_item('ITEM_ID_001', 'ITEM_MPN_001')
               .with_asset_item('ITEM_ID_001', 'ITEM_MPN_001_UPDATED')
               .with_asset_item_param('ITEM_ID_001', 'SOME_ITEM_PARAM_ID', 'ITEM_ID_001_PARAM_VALUE')
               .with_asset_item_param('ITEM_ID_001', 'SOME_ITEM_PARAM_ID', 'ITEM_ID_001_PARAM_VALUE_UPDATED')
               .with_asset_configuration_param('AS_CFG_ID_001', 'Cfg value', 'Cfg error value')
               .with_asset_configuration_param('AS_CFG_ID_001', 'Cfg value updated', 'Cfg error value updated'))

    assert request.is_asset_request()

    request = request.build()

    assert request['id'] == 'PR-0000-0000-0000-100'
    assert request['type'] == 'purchase'
    assert request['status'] == 'approved'

    assert request['asset']['id'] == 'AS-0000-0000-1000'
    assert request['asset']['status'] == 'active'

    assert request['asset']['marketplace']['id'] == 'MP-12345'

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


def test_request_builder_should_build_successfully_a_valid_tier_config_request():
    request = (fixtures.make_request_builder()
               .with_type('setup')
               .with_status('approved')
               .with_id('TCR-000-000-000-100')
               .with_tier_configuration_id('TC-000-000-000')
               .with_tier_configuration_status('active')
               .with_tier_configuration_marketplace('MP-12345')
               .with_tier_configuration_product('PRD-000-000-100', 'disabled')
               .with_tier_configuration_account('TA-0000-0000-1000')
               .with_tier_configuration_tier_level(2)
               .with_tier_configuration_param('PARAM_ID_001', 'VALUE_001')
               .with_tier_configuration_param('PARAM_ID_002', 'VALUE_002')
               .with_tier_configuration_param('PARAM_ID_003', '', 'Some value error on configuration')
               .with_tier_configuration_param('PARAM_ID_001', 'VALUE_001_UPDATED'))

    assert request.is_tier_config_request()

    request = request.build()

    assert request['id'] == 'TCR-000-000-000-100'
    assert request['type'] == 'setup'
    assert request['status'] == 'approved'

    assert request['configuration']['id'] == 'TC-000-000-000'
    assert request['configuration']['status'] == 'active'

    assert request['configuration']['marketplace']['id'] == 'MP-12345'

    assert request['configuration']['product']['id'] == 'PRD-000-000-100'
    assert request['configuration']['product']['status'] == 'disabled'

    assert request['configuration']['account']['id'] == 'TA-0000-0000-1000'

    assert request['configuration']['tier_level'] == 2

    assert request['configuration']['params'][0]['id'] == 'PARAM_ID_001'
    assert request['configuration']['params'][0]['value'] == 'VALUE_001_UPDATED'

    assert request['configuration']['params'][1]['id'] == 'PARAM_ID_002'
    assert request['configuration']['params'][1]['value'] == 'VALUE_002'

    assert request['configuration']['params'][2]['id'] == 'PARAM_ID_003'
    assert request['configuration']['params'][2]['value'] == ''
    assert request['configuration']['params'][2]['value_error'] == 'Some value error on configuration'

    assert request['params'][0]['id'] == 'PARAM_ID_001'
    assert request['params'][0]['value'] == 'VALUE_001_UPDATED'

    assert request['params'][1]['id'] == 'PARAM_ID_002'
    assert request['params'][1]['value'] == 'VALUE_002'

    assert request['params'][2]['id'] == 'PARAM_ID_003'
    assert request['params'][2]['value'] == ''
    assert request['params'][2]['value_error'] == 'Some value error on configuration'


def test_request_builder_should_build_successfully_a_valid_request_from_file_template():
    template = os.path.dirname(__file__) + TPL_REQUEST_ASSET

    request = (fixtures.make_request_builder(template)
               .build())

    assert request['id'] == 'PR-7658-9572-0778-001'
    assert request['type'] == 'purchase'
    assert request['status'] == 'pending'

    assert request['asset']['id'] == 'AS-7658-9572-0778'
    assert request['asset']['status'] == 'processing'


def test_request_dispatcher_should_create_successfully_a_asset_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + TPL_REQUEST_ASSET

    request = fixtures.make_request_builder(template)

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

    request = (fixtures.make_request_dispatcher(client=connect_client)
               .provision_request(request=to_create, timeout=0, max_attempt=1))

    assert isinstance(request, dict)


def test_request_dispatcher_should_update_successfully_a_asset_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + TPL_REQUEST_ASSET

    request = fixtures.make_request_builder(template)

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

    request = (fixtures.make_request_dispatcher(client=connect_client)
               .provision_request(request=to_update, timeout=0, max_attempt=1))

    assert request['asset']['params'][0]['value'] == 'SOME_VALID_VALUE'


def test_request_dispatcher_should_avoid_update_a_unchanged_asset_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + TPL_REQUEST_ASSET

    request = fixtures.make_request_builder(template)

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

    request = (fixtures.make_request_dispatcher(client=connect_client)
               .provision_request(request=to_update, timeout=0, max_attempt=1))

    assert request['asset']['params'][0]['value'] == ''


def test_request_dispatcher_should_create_successfully_a_tier_config_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + TPL_REQUEST_TIER_CONFIG

    request = fixtures.make_request_builder(template)

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

    request = (fixtures.make_request_dispatcher(client=connect_client)
               .provision_request(request=to_create, timeout=0, max_attempt=1))

    assert isinstance(request, dict)


def test_request_dispatcher_should_update_successfully_a_tier_config_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + TPL_REQUEST_TIER_CONFIG

    request = fixtures.make_request_builder(template)

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

    request = (fixtures.make_request_dispatcher(client=connect_client)
               .provision_request(request=to_update, timeout=0, max_attempt=1))

    assert isinstance(request, dict)
    assert request['configuration']['params'][0]['value'] == '111111'


def test_request_dispatcher_should_avoid_update_a_unchanged_tier_config_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + TPL_REQUEST_TIER_CONFIG

    request = fixtures.make_request_builder(template)

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

    request = (fixtures.make_request_dispatcher(client=connect_client)
               .provision_request(request=to_update, timeout=0, max_attempt=1))

    assert request['configuration']['params'][0]['value'] == '000000'
