import pytest

from connect.devops_testing.bdd.fixtures import use_connect_request_builder, use_connect_request_dispatcher
from connect.devops_testing.bdd.steps import (
    tier_config_request, asset_request, with_tier_config_account, with_id, with_product_id,
    with_marketplace_id, with_reseller_level, with_parameter_with_value, with_parameter_with_value_error,
    request_status_is, parameter_value_is, parameter_value_error_is, request_is_processed, with_status,
    subscription_request_is_processed, tier_configuration_request_is_processed, parameter_value_contains,
    parameter_value_error_contains, parameter_value_match, parameter_value_error_match, with_parameter_checked,
    with_parameter_not_checked, with_parameter_without_value, with_parameter_without_value_error,
    with_asset_tier_customer, with_asset_tier_tier1, with_asset_tier_tier2,
)

PARAM_ID_A = 'PARAM_ID_A'
PARAM_ID_A_VALUE = 'Some value A'
PARAM_ID_A_VALUE_ERROR = 'Some value error A'
PARAM_ID_CHECK = 'PARAM_ID_CHECK'
PARAM_ID_CHECK_VALUE = 'a|b|c'
PARAM_ID_CHECK_VALUE_NOT = 'a'
PARAM_ID_NO_VALUE = 'PARAM_ID_NO_VALUE'
PATTERN = r'^S[\s\w]*A$'


def test_step_should_raise_exception_on_undefined_request_type(behave_context):
    with pytest.raises(ValueError):
        use_connect_request_builder(context=behave_context)
        behave_context.request = {}

        parameter_value_is(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE)


def test_step_should_create_a_tier_configuration_request(behave_context):
    use_connect_request_builder(context=behave_context)

    tier_config_request(behave_context)
    with_id(behave_context, 'TCR-000-000-000-000')
    with_status(behave_context, 'pending')
    with_product_id(behave_context, 'PRD-000-000-000')
    with_marketplace_id(behave_context, 'MP-00000')
    with_tier_config_account(behave_context, 'TA-0000-0000-0000')
    with_reseller_level(behave_context, 2)
    with_parameter_with_value(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE)
    with_parameter_with_value_error(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE_ERROR)
    with_parameter_without_value(behave_context, PARAM_ID_NO_VALUE)
    with_parameter_without_value_error(behave_context, PARAM_ID_NO_VALUE)

    request = behave_context.builder.build()

    assert request['id'] == 'TCR-000-000-000-000'
    assert request['status'] == 'pending'
    assert request['type'] == 'setup'
    assert request['configuration']['product']['id'] == 'PRD-000-000-000'
    assert request['configuration']['account']['id'] == 'TA-0000-0000-0000'
    assert request['configuration']['marketplace']['id'] == 'MP-00000'
    assert request['configuration']['tier_level'] == 2
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
    with_status(behave_context, 'approved')
    with_parameter_with_value(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE)
    with_parameter_with_value_error(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE_ERROR)
    with_parameter_checked(behave_context, PARAM_ID_CHECK, PARAM_ID_CHECK_VALUE)
    with_parameter_not_checked(behave_context, PARAM_ID_CHECK, PARAM_ID_CHECK_VALUE_NOT)

    behave_context.request = behave_context.builder.build()

    request_status_is(behave_context, 'approved')
    parameter_value_is(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE)
    parameter_value_contains(behave_context, PARAM_ID_A, 'value')
    parameter_value_match(behave_context, PARAM_ID_A, PATTERN)
    parameter_value_error_is(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE_ERROR)
    parameter_value_error_contains(behave_context, PARAM_ID_A, 'error')
    parameter_value_error_match(behave_context, PARAM_ID_A, PATTERN)
    parameter_value_is(behave_context, PARAM_ID_CHECK, 'b|c')


def test_step_should_create_an_asset_request(behave_context):
    use_connect_request_builder(context=behave_context)

    asset_request(behave_context)
    with_id(behave_context, 'PR-000-000-000-000')
    with_status(behave_context, 'pending')
    with_product_id(behave_context, 'PRD-000-000-000')
    with_marketplace_id(behave_context, 'MP-00000')
    with_asset_tier_customer(behave_context, 'TA-0000-0000-0000')
    with_asset_tier_tier1(behave_context, 'TA-0000-0000-0001')
    with_asset_tier_tier2(behave_context, 'TA-0000-0000-0002')
    with_parameter_with_value(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE)
    with_parameter_with_value_error(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE_ERROR)
    with_parameter_without_value(behave_context, PARAM_ID_NO_VALUE)
    with_parameter_without_value_error(behave_context, PARAM_ID_NO_VALUE)

    request = behave_context.builder.build()

    assert request['id'] == 'PR-000-000-000-000'
    assert request['status'] == 'pending'
    assert request['type'] == 'purchase'
    assert request['asset']['product']['id'] == 'PRD-000-000-000'
    assert request['asset']['marketplace']['id'] == 'MP-00000'
    assert request['asset']['tiers']['customer']['id'] == 'TA-0000-0000-0000'
    assert request['asset']['tiers']['tier1']['id'] == 'TA-0000-0000-0001'
    assert request['asset']['tiers']['tier2']['id'] == 'TA-0000-0000-0002'
    assert request['asset']['params'][0]['id'] == PARAM_ID_A
    assert request['asset']['params'][0]['value'] == PARAM_ID_A_VALUE
    assert request['asset']['params'][0]['value_error'] == PARAM_ID_A_VALUE_ERROR
    assert request['asset']['params'][1]['id'] == PARAM_ID_NO_VALUE
    assert 'value' not in request['asset']['params'][1]
    assert 'value_error' not in request['asset']['params'][1]


def test_step_should_assert_successfully_an_asset_request(behave_context):
    use_connect_request_builder(context=behave_context)

    asset_request(behave_context)
    with_id(behave_context, 'PR-000-000-000-000')
    with_status(behave_context, 'pending')
    with_parameter_with_value(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE)
    with_parameter_with_value_error(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE_ERROR)
    with_parameter_checked(behave_context, PARAM_ID_CHECK, PARAM_ID_CHECK_VALUE)
    with_parameter_not_checked(behave_context, PARAM_ID_CHECK, PARAM_ID_CHECK_VALUE_NOT)

    behave_context.request = behave_context.builder.build()

    request_status_is(behave_context, 'pending')
    parameter_value_is(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE)
    parameter_value_contains(behave_context, PARAM_ID_A, 'value')
    parameter_value_match(behave_context, PARAM_ID_A, PATTERN)
    parameter_value_error_is(behave_context, PARAM_ID_A, PARAM_ID_A_VALUE_ERROR)
    parameter_value_error_contains(behave_context, PARAM_ID_A, 'error')
    parameter_value_error_match(behave_context, PARAM_ID_A, PATTERN)
    parameter_value_is(behave_context, PARAM_ID_CHECK, 'b|c')


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
