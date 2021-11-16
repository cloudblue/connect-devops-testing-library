from connect.devops_testing import asserts

asset_request = {
    'status': 'approved',
    'type': 'purchase',
    'reason': 'some reason',
    'note': 'some note',
    'asset': {
        'status': 'active',
        'params': [
            {'id': 'ID', 'value': 'value', 'value_error': 'some error'},
            {'id': 'ID_2', 'value': '42', 'value_error': ''},
        ],
    }
}
config_request = {
    'status': 'pending',
    'type': 'setup',
    'configuration': {
        'status': 'active',
        'params': [
            {'id': 'ID', 'value': 'value', 'value_error': 'some error'},
            {'id': 'ID_2', 'value': '42', 'value_error': ''},
        ],
    }
}


def test_should_assert_request_status():
    asserts.request_status(asset_request, 'approved')


def test_should_assert_task_response_status():
    class TaskResponse(object):
        def __init__(self, status: str):
            self.status = status

    asserts.task_response_status(TaskResponse('success'), 'success')


def test_should_assert_request_note():
    asserts.request_note(asset_request, 'some note')


def test_should_assert_request_reason():
    asserts.request_reason(asset_request, 'some reason')


def test_should_assert_asset_status():
    asserts.asset_status(asset_request, 'active')


def test_should_assert_asset_params_value_equal():
    asserts.asset_params_value_equal(asset_request, 'ID', 'value')


def test_should_assert_asset_params_value_not_equal():
    asserts.asset_params_value_not_equal(asset_request, 'ID', 'other')


def test_should_assert_asset_params_value_contains():
    asserts.asset_params_value_contains(asset_request, 'ID', 'value')


def test_should_assert_asset_params_value_equal_error():
    asserts.asset_params_value_equal_error(asset_request, 'ID', 'some error')


def test_should_assert_asset_params_value_not_equal_error():
    asserts.asset_params_value_not_equal_error(asset_request, 'ID', 'other error')


def test_should_assert_asset_params_value_contains_error():
    asserts.asset_params_value_contains_error(asset_request, 'ID', 'some error')
    asserts.asset_params_value_contains_error(asset_request, 'ID', 'some')


def test_should_assert_tier_configuration_status():
    asserts.tier_configuration_status(config_request, 'active')


def test_should_assert_tier_configuration_params_value_equal():
    asserts.tier_configuration_params_value_equal(config_request, 'ID', 'value')


def test_should_assert_tier_configuration_params_value_not_equal():
    asserts.tier_configuration_params_value_not_equal(config_request, 'ID', 'other')


def test_should_assert_tier_configuration_params_value_contains():
    asserts.tier_configuration_params_value_contains(config_request, 'ID', 'value')


def test_should_assert_tier_configuration_params_value_equal_error():
    asserts.tier_configuration_params_value_equal_error(config_request, 'ID', 'some error')


def test_should_assert_tier_configuration_params_value_not_equal_error():
    asserts.tier_configuration_params_value_not_equal_error(config_request, 'ID', 'other error')


def test_should_assert_tier_configuration_params_value_contains_error():
    asserts.tier_configuration_params_value_contains_error(config_request, 'ID', 'some error')
    asserts.tier_configuration_params_value_contains_error(config_request, 'ID', 'some')
