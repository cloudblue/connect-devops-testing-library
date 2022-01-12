from behave import step
from behave.runner import Context

from collections.abc import Callable

from connect.devops_testing import asserts
from connect.devops_testing.utils import request_model


def _get_request_handler(asset: Callable, tier_config: Callable, request_type: str) -> Callable:
    def _raise_exception_on_request(*args, **kwargs):
        raise ValueError('Invalid request type.')

    strategies = {
        'asset': asset,
        'tier-config': tier_config,
        'undefined': _raise_exception_on_request,
    }

    return strategies.get(request_type)


def _request_is_process(context: Context):
    if isinstance(context.request, dict) and context.request.get('id') is not None:
        context.builder.with_id(context.request.get('id'))

    context.request.update(context.builder.build())
    context.request.update(context.connect.provision_request(
        request=context.request,
    ))
    print(f"Processed request id: {context.request.get('id')}")


def _with_checkbox_parameter(context: Context, parameter: str, values: str, checked: bool):
    handler = _get_request_handler(
        asset=context.builder.with_asset_param,
        tier_config=context.builder.with_tier_configuration_param,
        request_type=context.builder.request_type(),
    )

    handler(
        param_id=context.parameter(parameter),
        value={context.value(value): checked for value in values.split("|")},
        value_type='checkbox',
    )


def _with_parameter_without_value(context: Context, parameter: str):
    handler = _get_request_handler(
        asset=context.builder.with_asset_param,
        tier_config=context.builder.with_tier_configuration_param,
        request_type=context.builder.request_type(),
    )

    handler(param_id=context.parameter(parameter))


def _with_item(context: Context, item_id: str, item_mpn: str, quantity: str):
    context.builder.with_asset_item(
        item_id=context.shared(item_id),
        item_mpn=context.shared(item_mpn),
        quantity=context.shared(quantity),
    )


@step('request is processed')
def request_is_processed(context: Context):
    _request_is_process(context)


@step('subscription request is processed')
def subscription_request_is_processed(context: Context):
    _request_is_process(context)


@step('tier configuration request is processed')
def tier_configuration_request_is_processed(context: Context):
    _request_is_process(context)


@step('tier config request')
def tier_config_request(context: Context):
    context.builder = context.builder.from_default_tier_config()
    context.builder = context.builder.with_tier_configuration_account('random')


@step('asset request')
def asset_request(context: Context):
    context.builder = context.builder.from_default_asset()
    context.builder = context.builder.with_asset_tier_customer('random')
    context.builder = context.builder.with_asset_tier_tier1('random')
    context.builder = context.builder.with_asset_external_id('random')
    context.builder = context.builder.with_asset_external_uid('random')


@step('request with id "{request_id}"')
def with_id(context: Context, request_id: str):
    context.builder.with_id(context.shared(request_id))


@step('request with type "{request_type}"')
def with_type(context: Context, request_type: str):
    context.builder.with_type(context.shared(request_type))


@step('request with status "{request_status}"')
def with_status(context: Context, request_status: str):
    context.builder.with_status(request_status)


@step('request with reason "{reason}"')
def with_reason(context: Context, reason: str):
    context.builder.with_reason(context.value(reason.strip()))


@step('request with note "{note}"')
def with_note(context: Context, note: str):
    context.builder.with_note(context.value(note.strip()))


@step('request with configuration account "{account_id}"')
def with_tier_config_account(context: Context, account_id: str):
    context.builder.with_tier_configuration_account(context.shared(account_id))


@step('request with tier config id "{tier_config_id}"')
def with_tier_config_id(context: Context, tier_config_id: str):
    context.builder.with_tier_configuration_id(context.shared(tier_config_id))


@step('request with asset id "{asset_id}"')
def with_asset_id(context: Context, asset_id: str):
    context.builder.with_asset_id(context.shared(asset_id))


@step('request with asset external id "{external_id}"')
def with_asset_external_id(context: Context, external_id: str):
    context.builder.with_asset_external_id(context.shared(external_id))


@step('request with asset external uid "{external_uid}"')
def with_asset_external_uid(context: Context, external_uid: str):
    context.builder.with_asset_external_uid(context.shared(external_uid))


@step('request with asset customer "{customer_id}"')
def with_asset_tier_customer(context: Context, customer_id: str):
    context.builder.with_asset_tier_customer(context.shared(customer_id))


@step('request with asset tier1 "{tier1_id}"')
def with_asset_tier_tier1(context: Context, tier1_id: str):
    context.builder.with_asset_tier_tier1(context.shared(tier1_id))


@step('request with asset tier2 "{tier2_id}"')
def with_asset_tier_tier2(context: Context, tier2_id: str):
    context.builder.with_asset_tier_tier2(context.shared(tier2_id))


@step('request with asset "{tier}" from country "{country}"')
def with_asset_tier_from_country(context: Context, tier: str, country: str):
    context.builder.with_asset_tier(tier_name=tier, tier={
        "contact_info": {
            "country": context.shared(country),
        },
    })


@step('request with product "{product_id}"')
def with_product_id(context: Context, product_id: str):
    handler = _get_request_handler(
        asset=context.builder.with_asset_product,
        tier_config=context.builder.with_tier_configuration_product,
        request_type=context.builder.request_type(),
    )

    handler(product_id=context.shared(product_id))


@step('request with marketplace "{marketplace_id}"')
def with_marketplace_id(context: Context, marketplace_id: str):
    handler = _get_request_handler(
        asset=context.builder.with_asset_marketplace,
        tier_config=context.builder.with_tier_configuration_marketplace,
        request_type=context.builder.request_type(),
    )

    handler(marketplace_id=context.shared(marketplace_id))


@step('request with connection "{connection_id}" of type "{connection_type}"')
def with_connection_id(context: Context, connection_id: str, connection_type: str):
    handler = _get_request_handler(
        asset=context.builder.with_asset_connection,
        tier_config=context.builder.with_tier_configuration_connection,
        request_type=context.builder.request_type(),
    )

    handler(
        connection_id=context.shared(connection_id),
        connection_type=context.shared(connection_type),
    )


@step('request with reseller level "{level}"')
def with_reseller_level(context: Context, level: str):
    context.builder.with_tier_configuration_tier_level(context.shared(level))


@step('request with parameter "{parameter}" with value "{value}"')
def with_parameter_with_value(context: Context, parameter: str, value: str = ''):
    handler = _get_request_handler(
        asset=context.builder.with_asset_param,
        tier_config=context.builder.with_tier_configuration_param,
        request_type=context.builder.request_type(),
    )

    handler(
        param_id=context.parameter(parameter),
        value=context.value(value.strip()),
    )


@step('request with parameter "{parameter}" value "{values}" checked')
def with_parameter_checked(context: Context, parameter: str, values: str):
    _with_checkbox_parameter(context, parameter, values, True)


@step('request with parameter "{parameter}" value "{values}" not checked')
def with_parameter_not_checked(context: Context, parameter: str, values: str):
    _with_checkbox_parameter(context, parameter, values, False)


@step('request with parameter "{parameter}" without value')
def with_parameter_without_value(context: Context, parameter: str):
    _with_parameter_without_value(context, parameter)


@step('request with parameter "{parameter}" with value error "{value}"')
def with_parameter_with_value_error(context: Context, parameter: str, value: str = ''):
    handler = _get_request_handler(
        asset=context.builder.with_asset_param,
        tier_config=context.builder.with_tier_configuration_param,
        request_type=context.builder.request_type(),
    )

    handler(
        param_id=context.parameter(parameter),
        value_error=context.value(value.strip()),
    )


@step('request with parameter "{parameter}" without value error')
def with_parameter_without_value_error(context: Context, parameter: str):
    _with_parameter_without_value(context, parameter)


@step('request with item "{item_id}" with mpn "{item_mpn}" x{quantity}')
def with_item_quantity(context: Context, item_id: str, item_mpn: str, quantity: str):
    _with_item(context, item_id, item_mpn, quantity)


@step('request with items')
def with_items(context: Context):
    for row in context.table:
        _with_item(context, row['item'], row['mpn'], row['quantity'])


@step('request parameter "{parameter}" value is "{value}"')
def parameter_value_is(context: Context, parameter: str, value: str):
    handler = _get_request_handler(
        asset=asserts.asset_param_value_equal,
        tier_config=asserts.tier_configuration_param_value_equal,
        request_type=request_model(context.request),
    )

    handler(
        request=context.request,
        param_id=context.parameter(parameter),
        expected=context.value(value.strip()),
    )


@step('request parameter "{parameter}" value contains "{value}"')
def parameter_value_contains(context: Context, parameter: str, value: str):
    handler = _get_request_handler(
        asset=asserts.asset_param_value_contains,
        tier_config=asserts.tier_configuration_param_value_contains,
        request_type=request_model(context.request),
    )

    handler(
        request=context.request,
        param_id=context.parameter(parameter),
        expected=context.value(value.strip()),
    )


@step('request parameter "{parameter}" value match "{pattern}"')
def parameter_value_match(context: Context, parameter: str, pattern: str):
    handler = _get_request_handler(
        asset=asserts.asset_param_value_match,
        tier_config=asserts.tier_configuration_param_value_match,
        request_type=request_model(context.request),
    )

    handler(
        request=context.request,
        param_id=context.parameter(parameter),
        pattern=context.value(pattern.strip()),
    )


@step('request parameter "{parameter}" value error is "{value_error}"')
def parameter_value_error_is(context: Context, parameter: str, value_error: str):
    handler = _get_request_handler(
        asset=asserts.asset_param_value_error_equal,
        tier_config=asserts.tier_configuration_param_value_error_equal,
        request_type=request_model(context.request),
    )

    handler(
        request=context.request,
        param_id=context.parameter(parameter),
        expected=context.value(value_error.strip()),
    )


@step('request parameter "{parameter}" value error contains "{value_error}"')
def parameter_value_error_contains(context: Context, parameter: str, value_error: str):
    handler = _get_request_handler(
        asset=asserts.asset_param_value_error_contains,
        tier_config=asserts.tier_configuration_param_value_error_contains,
        request_type=request_model(context.request),
    )

    handler(
        request=context.request,
        param_id=context.parameter(parameter),
        expected=context.value(value_error.strip()),
    )


@step('request parameter "{parameter}" value error match "{pattern}"')
def parameter_value_error_match(context: Context, parameter: str, pattern: str):
    handler = _get_request_handler(
        asset=asserts.asset_param_value_error_match,
        tier_config=asserts.tier_configuration_param_value_error_match,
        request_type=request_model(context.request),
    )

    handler(
        request=context.request,
        param_id=context.parameter(parameter),
        pattern=context.value(pattern.strip()),
    )


@step('request status is "{request_status}"')
def request_status_is(context: Context, request_status):
    asserts.request_status(context.request, request_status)


@step('request reason is "{reason}"')
def request_reason_is(context: Context, reason: str):
    asserts.request_reason(context.request, context.value(reason))


@step('request note is "{note}"')
def request_note_is(context: Context, note: str):
    asserts.request_note(context.request, context.value(note))
