from hoare import asserts

request = {'asset': {'params': [{'id': 'ID', 'value': 'value', 'value_error': 'some error'}]}}


def test_should_assert_request_status():
    asserts.request_status({'status': 'approved'}, 'approved')


def test_should_task_response_status():
    class TaskResponse(object):
        def __init__(self, status: str):
            self.status = status

    asserts.task_response_status(TaskResponse('success'), 'success')


def test_should_asset_status():
    asserts.asset_status({'asset': {'status': 'active'}}, 'active')


def test_should_asset_params_value_equal():
    asserts.asset_params_value_equal(request, 'ID', 'value')


def test_should_asset_params_value_not_equal():
    asserts.asset_params_value_not_equal(request, 'ID', 'other')


def test_should_asset_params_value_contains():
    asserts.asset_params_value_contains(request, 'ID', ['value'])


def test_should_asset_params_value_equal_error():
    asserts.asset_params_value_equal_error(request, 'ID', 'some error')


def test_should_asset_params_value_not_equal_error():
    asserts.asset_params_value_not_equal_error(request, 'ID', 'other error')


def test_should_asset_params_value_contains_error():
    asserts.asset_params_value_contains_error(request, 'ID', ['some error'])
