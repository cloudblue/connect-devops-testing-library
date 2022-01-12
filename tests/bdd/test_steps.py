import pytest

from connect.devops_testing.bdd.fixtures import use_connect_request_builder, use_connect_request_dispatcher
from connect.devops_testing.bdd.steps import (
    tier_config_request, asset_request, with_tier_config_account, with_id, with_product_id,
    with_marketplace_id, with_reseller_level, with_parameter_with_value, with_parameter_with_value_error,
    request_status_is, parameter_value_is, parameter_value_error_is, request_is_processed, with_status,
    subscription_request_is_processed, tier_configuration_request_is_processed, parameter_value_contains,
    parameter_value_error_contains, parameter_value_match, parameter_value_error_match, with_parameter_checked,
    with_parameter_not_checked, with_parameter_without_value, with_parameter_without_value_error,
    with_asset_tier_customer, with_asset_tier_tier1, with_asset_tier_tier2, with_connection_id, with_item_quantity,
    with_items, request_note_is, request_reason_is, with_note, with_reason, with_asset_tier_from_country,
    with_asset_external_id, with_asset_external_uid, with_tier_config_id, with_asset_id, with_type,
)

PARAM_ID_A = 'PARAM_ID_A'
PARAM_ID_A_VALUE = 'Some value A'
PARAM_ID_A_VALUE_ERROR = 'Some value error A'
PARAM_ID_CHECK = 'PARAM_ID_CHECK'
PARAM_ID_CHECK_VALUE = 'a|b|c'
PARAM_ID_CHECK_VALUE_NOT = 'a'
PARAM_ID_NO_VALUE = 'PARAM_ID_NO_VALUE'
PATTERN = r'^S[\s\w]*A$'
NOTE = 'Some note'
REASON = 'Some reason'


def _shared_assert_steps(behave_context):
    request_note_is(behave_context, NOTE)
    request_reason_is(behave_context, REASON)
    parameter_value_is(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE)
    parameter_value_contains(behave_context, PARAM_ID_A, 'value')
    parameter_value_match(behave_context, PARAM_ID_A, PATTERN)
    parameter_value_error_is(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE_ERROR)
    parameter_value_error_contains(behave_context, PARAM_ID_A, 'error')
    parameter_value_error_match(behave_context, PARAM_ID_A, PATTERN)
    parameter_value_is(behave_context, PARAM_ID_CHECK, 'b|c')


def test_step_should_raise_exception_on_undefined_request_type(behave_context):
    with pytest.raises(ValueError):
        use_connect_request_builder(context=behave_context)
        behave_context.request = {}

        parameter_value_is(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE)


def test_step_should_create_a_tier_configuration_request(behave_context):
    use_connect_request_builder(context=behave_context)

    tier_config_request(behave_context)
    with_id(behave_context, 'TCR-000-000-000-000')
    with_type(behave_context, 'setup')
    with_note(behave_context, NOTE)
    with_reason(behave_context, REASON)
    with_status(behave_context, 'pending')
    with_tier_config_id(behave_context, 'TC-000-000-000')
    with_product_id(behave_context, 'PRD-000-000-000')
    with_marketplace_id(behave_context, 'MP-00000')
    with_connection_id(behave_context, 'CT-0000-0000-0000', 'test')
    with_tier_config_account(behave_context, 'TA-0000-0000-0000')
    with_reseller_level(behave_context, "2")
    with_parameter_with_value(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE)
    with_parameter_with_value_error(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE_ERROR)
    with_parameter_without_value(behave_context, PARAM_ID_NO_VALUE)
    with_parameter_without_value_error(behave_context, PARAM_ID_NO_VALUE)

    request = behave_context.builder.build()

    assert request['id'] == 'TCR-000-000-000-000'
    assert request['status'] == 'pending'
    assert request['type'] == 'setup'
    assert request['note'] == NOTE
    assert request['reason'] == REASON
    assert request['configuration']['product']['id'] == 'PRD-000-000-000'
    assert request['configuration']['account']['id'] == 'TA-0000-0000-0000'
    assert request['configuration']['marketplace']['id'] == 'MP-00000'
    assert request['configuration']['connection']['id'] == 'CT-0000-0000-0000'
    assert request['configuration']['connection']['type'] == 'test'
    assert request['configuration']['tier_level'] == "2"
    assert request['configuration']['params'][0]['id'] == PARAM_ID_A
    assert request['configuration']['params'][0]['value'] == PARAM_ID_A_VALUE
    assert request['configuration']['params'][0]['value_error'] == PARAM_ID_A_VALUE_ERROR
    assert request['params'][0]['id'] == PARAM_ID_A
    assert request['params'][0]['value'] == PARAM_ID_A_VALUE
    assert request['params'][0]['value_error'] == PARAM_ID_A_VALUE_ERROR
    assert request['params'][1]['id'] == PARAM_ID_NO_VALUE
    assert 'value' not in request['params'][1]
    assert 'value_error' not in request['params'][1]


def test_step_should_assert_successfully_a_tier_configuration_request(behave_context):
    use_connect_request_builder(context=behave_context)

    tier_config_request(behave_context)
    with_id(behave_context, 'TCR-000-000-000-000')
    with_note(behave_context, NOTE)
    with_reason(behave_context, REASON)
    with_status(behave_context, 'approved')
    with_parameter_with_value(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE)
    with_parameter_with_value_error(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE_ERROR)
    with_parameter_checked(behave_context, PARAM_ID_CHECK, PARAM_ID_CHECK_VALUE)
    with_parameter_not_checked(behave_context, PARAM_ID_CHECK, PARAM_ID_CHECK_VALUE_NOT)

    behave_context.request = behave_context.builder.build()

    request_status_is(behave_context, 'approved')
    _shared_assert_steps(behave_context)


def test_step_should_create_an_asset_request(behave_context):
    use_connect_request_builder(
        context=behave_context,
        parameters={'PARAM_ID_A': PARAM_ID_A},
        values={'PARAM_ID_A_VALUE': PARAM_ID_A_VALUE},
        shared={'CONNECTION_ID': 'CT-0000-0000-0000'},
    )

    asset_request(behave_context)
    with_id(behave_context, 'PR-000-000-000-000')
    with_type(behave_context, 'change')
    with_status(behave_context, 'pending')
    with_product_id(behave_context, 'PRD-000-000-000')
    with_note(behave_context, NOTE)
    with_reason(behave_context, REASON)
    with_asset_id(behave_context, 'AS-000-000-000')
    with_marketplace_id(behave_context, 'MP-00000')
    with_connection_id(behave_context, 'CONNECTION_ID', 'test')
    with_asset_external_id(behave_context, '123456789')
    with_asset_external_uid(behave_context, '9fb50525-a4a4-41a7-ace0-dc3c73796d32')
    with_asset_tier_customer(behave_context, 'random')
    with_asset_tier_from_country(behave_context, 'customer', 'US')
    with_asset_tier_tier1(behave_context, 'TA-0000-0000-0001')
    with_asset_tier_tier2(behave_context, 'TA-0000-0000-0002')
    with_parameter_with_value(behave_context, 'PARAM_ID_A', 'PARAM_ID_A_VALUE')
    with_parameter_with_value_error(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE_ERROR)
    with_parameter_without_value(behave_context, PARAM_ID_NO_VALUE)
    with_parameter_without_value_error(behave_context, PARAM_ID_NO_VALUE)
    with_item_quantity(behave_context, 'ITEM_ID_001', 'ITEM_MPN_001', '41')

    behave_context.table = [
        {'item': 'ITEM_ID_002', 'mpn': 'ITEM_MPN_002', 'quantity': '42'},
        {'item': 'ITEM_ID_003', 'mpn': 'ITEM_MPN_003', 'quantity': '43'}
    ]
    with_items(behave_context)

    request = behave_context.builder.build()

    assert request['id'] == 'PR-000-000-000-000'
    assert request['status'] == 'pending'
    assert request['type'] == 'change'
    assert request['note'] == NOTE
    assert request['reason'] == REASON
    assert request['asset']['external_id'] == '123456789'
    assert request['asset']['external_uid'] == '9fb50525-a4a4-41a7-ace0-dc3c73796d32'
    assert request['asset']['product']['id'] == 'PRD-000-000-000'
    assert request['asset']['marketplace']['id'] == 'MP-00000'
    assert request['asset']['connection']['id'] == 'CT-0000-0000-0000'
    assert request['asset']['connection']['type'] == 'test'
    assert 'id' not in request['asset']['tiers']['customer']
    assert 'contact' in request['asset']['tiers']['customer']['contact_info']
    assert request['asset']['tiers']['customer']['contact_info']['country'] == 'US'
    assert request['asset']['tiers']['tier1']['id'] == 'TA-0000-0000-0001'
    assert 'type' not in request['asset']['tiers']['tier1']
    assert request['asset']['tiers']['tier2']['id'] == 'TA-0000-0000-0002'
    assert 'type' not in request['asset']['tiers']['tier2']
    assert request['asset']['params'][0]['id'] == PARAM_ID_A
    assert request['asset']['params'][0]['value'] == PARAM_ID_A_VALUE
    assert request['asset']['params'][0]['value_error'] == PARAM_ID_A_VALUE_ERROR
    assert request['asset']['params'][1]['id'] == PARAM_ID_NO_VALUE
    assert request['asset']['items'][0]['id'] == 'ITEM_ID_001'
    assert request['asset']['items'][0]['mpn'] == 'ITEM_MPN_001'
    assert request['asset']['items'][0]['quantity'] == '41'
    assert request['asset']['items'][1]['id'] == 'ITEM_ID_002'
    assert request['asset']['items'][1]['mpn'] == 'ITEM_MPN_002'
    assert request['asset']['items'][1]['quantity'] == '42'
    assert request['asset']['items'][2]['id'] == 'ITEM_ID_003'
    assert request['asset']['items'][2]['mpn'] == 'ITEM_MPN_003'
    assert request['asset']['items'][2]['quantity'] == '43'
    assert 'value' not in request['asset']['params'][1]
    assert 'value_error' not in request['asset']['params'][1]


def test_step_should_assert_successfully_an_asset_request(behave_context):
    use_connect_request_builder(context=behave_context)

    asset_request(behave_context)
    with_id(behave_context, 'PR-000-000-000-000')
    with_status(behave_context, 'pending')
    with_note(behave_context, NOTE)
    with_reason(behave_context, REASON)
    with_parameter_with_value(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE)
    with_parameter_with_value_error(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE_ERROR)
    with_parameter_checked(behave_context, PARAM_ID_CHECK, PARAM_ID_CHECK_VALUE)
    with_parameter_not_checked(behave_context, PARAM_ID_CHECK, PARAM_ID_CHECK_VALUE_NOT)

    behave_context.request = behave_context.builder.build()

    request_status_is(behave_context, 'pending')
    _shared_assert_steps(behave_context)


def test_step_should_successfully_process_the_request(sync_client_factory, response_factory, behave_context):
    process_steps = [
        request_is_processed,
        subscription_request_is_processed,
        tier_configuration_request_is_processed
    ]

    behave_context.request = {'id': 'PR-000-000-000-000'}

    for process_step in process_steps:
        use_connect_request_builder(context=behave_context)

        asset_request(behave_context)
        with_status(behave_context, 'pending')

        mocked_client = sync_client_factory([
            response_factory(value={'id': 'PR-000-000-000-000', 'type': 'purchase', 'status': 'pending'}),
            response_factory(value={'id': 'PR-000-000-000-000', 'type': 'purchase', 'status': 'approved'}),
        ])

        use_connect_request_dispatcher(context=behave_context, client=mocked_client)

        process_step(behave_context)

        assert behave_context.request['id'] == 'PR-000-000-000-000'
        assert behave_context.request['type'] == 'purchase'
        assert behave_context.request['status'] == 'approved'
