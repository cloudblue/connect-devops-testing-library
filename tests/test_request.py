from connect.devops_testing import fixures

import os


def test_request_builder_should_build_successfully_a_valid_request():
    request = fixures.make_request_builder() \
        .with_type('purchase') \
        .with_status('approved') \
        .with_id('PR-0000-0000-0000-100') \
        .with_asset_product('PRD-000-000-100', 'The Name', 'disabled') \
        .with_asset_id('AS-0000-0000-1000') \
        .with_asset_status('active') \
        .with_asset_param('PARAM_ID_001', 'VALUE_001') \
        .with_asset_param('PARAM_ID_002', 'VALUE_002') \
        .with_asset_param('PARAM_ID_003', '', 'Some value error') \
        .with_asset_param('PARAM_ID_001', 'VALUE_001_UPDATED') \
        .with_asset_item('ITEM_ID_001', 'ITEM_MPN_001') \
        .with_asset_item('ITEM_ID_001', 'ITEM_MPN_001_UPDATED') \
        .with_asset_item_param('ITEM_ID_001', 'SOME_ITEM_PARAM_ID', 'ITEM_ID_001_PARAM_VALUE') \
        .with_asset_item_param('ITEM_ID_001', 'SOME_ITEM_PARAM_ID', 'ITEM_ID_001_PARAM_VALUE_UPDATED') \
        .with_asset_configuration_param('AS_CFG_ID_001', 'Cfg value', 'Cfg error value') \
        .with_asset_configuration_param('AS_CFG_ID_001', 'Cfg value updated', 'Cfg error value updated') \
        .build()

    assert request['id'] == 'PR-0000-0000-0000-100'
    assert request['type'] == 'purchase'
    assert request['status'] == 'approved'

    assert request['asset']['id'] == 'AS-0000-0000-1000'
    assert request['asset']['status'] == 'active'

    assert request['asset']['product']['id'] == 'PRD-000-000-100'
    assert request['asset']['product']['name'] == 'The Name'
    assert request['asset']['product']['status'] == 'disabled'

    assert request['asset']['params'][0]['id'] == 'PARAM_ID_001'
    assert request['asset']['params'][0]['value'] == 'VALUE_001_UPDATED'

    assert request['asset']['params'][1]['id'] == 'PARAM_ID_002'
    assert request['asset']['params'][1]['value'] == 'VALUE_002'

    assert request['asset']['params'][2]['id'] == 'PARAM_ID_003'
    assert request['asset']['params'][2]['value'] == ''
    assert request['asset']['params'][2]['value_error'] == 'Some value error'

    assert request['asset']['items'][0]['id'] == 'ITEM_ID_001'
    assert request['asset']['items'][0]['mpn'] == 'ITEM_MPN_001_UPDATED'

    assert request['asset']['items'][0]['params'][0]['id'] == 'SOME_ITEM_PARAM_ID'
    assert request['asset']['items'][0]['params'][0]['value'] == 'ITEM_ID_001_PARAM_VALUE_UPDATED'

    assert request['asset']['configuration']['params'][0]['id'] == 'AS_CFG_ID_001'
    assert request['asset']['configuration']['params'][0]['value'] == 'Cfg value updated'
    assert request['asset']['configuration']['params'][0]['value_error'] == 'Cfg error value updated'


def test_request_builder_should_build_successfully_a_valid_request_from_file_template():
    template = os.path.dirname(__file__) + '/request.json'

    request = fixures.make_request_builder() \
        .from_file(template) \
        .build()

    assert request['id'] == 'PR-7658-9572-0778-001'
    assert request['type'] == 'purchase'
    assert request['status'] == 'pending'

    assert request['asset']['id'] == 'AS-7658-9572-0778'
    assert request['asset']['status'] == 'processing'


def test_request_dispatcher_should_provision_successfully_a_request(sync_client_factory, response_factory):
    template = os.path.dirname(__file__) + '/request.json'

    request = fixures.make_request_builder() \
        .from_file(template)

    pending = request.build()
    approved = request \
        .with_status('approved') \
        .with_asset_status('active') \
        .build()

    connect_client = sync_client_factory([
        response_factory(value=pending), # request.create
        response_factory(value=pending), # request.get (first call)
        response_factory(value=approved), # request.get (second call)
    ])

    request = fixures.make_request_dispatcher(client=connect_client) \
        .provision_request(request=pending, timeout=0, max_attempt=1)

    assert isinstance(request, dict)
