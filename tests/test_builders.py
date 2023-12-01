from connect.devops_testing.builders import AssetBuilder


def test_asset_builder_should_build_asset_with_id():
    asset = AssetBuilder().with_id('AS-0000-0000-1000').build()
    assert asset['id'] == 'AS-0000-0000-1000'


def test_asset_builder_should_build_valid_asset():
    builder = AssetBuilder()
    builder.with_id('AS-0000-0000-1000')
    builder.with_status('active')
    builder.with_external_id('123456789')
    builder.with_external_uid('9fb50525-a4a4-41a7-ace0-dc3c73796d32')
    builder.with_product('PRD-000-000-100', 'Product', 'published')
    builder.with_marketplace('MP-12345', 'Marketplace')
    builder.with_contract('CNT-000-000', 'distribution', 'Contract')
    builder.with_connection(
        connection_id='CT-0000-0000-0000',
        connection_type='test',
        provider={"id": "PA-800-926", "name": "IMC Gamma Team Provider"},
        vendor={"id": "VA-610-138", "name": "IMC Gamma Team Vendor"},
        hub={"id": "HB-0000-0000", "name": "None"},
    )
    builder.with_items([
        {
            'item_id': 'ITEM_ID_001',
            'item_mpn': 'ITEM_MPN_001',
            'params': [{'param_id': 'SOME_ITEM_PARAM_ID', 'value': 'ITEM_ID_001_PARAM_VALUE'}]
        },
        {
            'item_id': 'ITEM_ID_002',
            'item_mpn': 'ITEM_MPN_002',
        },
    ])
    builder.with_params([
        {'param_id': 'PARAM_ID_001', 'value': 'VALUE_001'},
        {'param_id': 'PARAM_ID_002', 'value': 'VALUE_002', 'value_error': 'param error value'},
    ])
    builder.with_configuration_params([
        {'param_id': 'AS_CFG_ID_001', 'value': 'Cfg value'},
        {'param_id': 'IS_A_LIST_001', 'value': [1, 2]},
    ])
    builder.with_tier_customer('random')
    builder.with_tier_tier1('random')
    builder.with_tier_tier2('random')

    asset = builder.build()

    assert asset['id'] == 'AS-0000-0000-1000'
    assert asset['status'] == 'active'

    assert asset['external_id'] == '123456789'
    assert asset['external_uid'] == '9fb50525-a4a4-41a7-ace0-dc3c73796d32'

    assert asset['product']['id'] == 'PRD-000-000-100'
    assert asset['product']['name'] == 'Product'
    assert asset['product']['status'] == 'published'

    assert asset['marketplace']['id'] == 'MP-12345'
    assert asset['marketplace']['name'] == 'Marketplace'

    assert asset['contract']['id'] == 'CNT-000-000'
    assert asset['contract']['type'] == 'distribution'
    assert asset['contract']['name'] == 'Contract'

    assert asset['connection']['id'] == 'CT-0000-0000-0000'
    assert asset['connection']['type'] == 'test'
    assert asset['connection']['provider']['id'] == 'PA-800-926'
    assert asset['connection']['provider']['name'] == 'IMC Gamma Team Provider'
    assert asset['connection']['vendor']['id'] == 'VA-610-138'
    assert asset['connection']['vendor']['name'] == 'IMC Gamma Team Vendor'
    assert asset['connection']['hub']['id'] == 'HB-0000-0000'
    assert asset['connection']['hub']['name'] == 'None'

    assert asset['items'][0]['id'] == 'ITEM_ID_001'
    assert asset['items'][0]['mpn'] == 'ITEM_MPN_001'

    assert asset['items'][0]['params'][0]['id'] == 'SOME_ITEM_PARAM_ID'
    assert asset['items'][0]['params'][0]['value'] == 'ITEM_ID_001_PARAM_VALUE'

    assert asset['params'][0]['id'] == 'PARAM_ID_001'
    assert asset['params'][0]['value'] == 'VALUE_001'

    assert asset['params'][1]['id'] == 'PARAM_ID_002'
    assert asset['params'][1]['value'] == 'VALUE_002'
    assert asset['params'][1]['value_error'] == 'param error value'

    assert asset['configuration']['params'][0]['id'] == 'AS_CFG_ID_001'
    assert asset['configuration']['params'][0]['value'] == 'Cfg value'

    assert asset['configuration']['params'][1]['id'] == 'IS_A_LIST_001'
    assert asset['configuration']['params'][1]['structured_value'] == [1, 2]

    assert asset['tiers']['customer']['type'] == 'customer'
    assert asset['tiers']['tier1']['type'] == 'reseller'
    assert asset['tiers']['tier2']['type'] == 'reseller'


