from hoare import fixures


def test_should_build_successfully_a_valid_request():
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
