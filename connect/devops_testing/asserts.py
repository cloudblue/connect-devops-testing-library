import operator
from typing import Any

from connect.devops_testing.utils import find_by_id

__operators = {
    '==': operator.eq,
    '!=': operator.ne,
    'in': operator.contains,
}


def request_status(request: dict, expected: str):
    assert request['status'] == expected


def task_response_status(task_response, expected: str):
    assert task_response.status == expected


def asset_status(request: dict, expected: str):
    assert request['asset']['status'] == expected


def asset_params_value(request: dict, param_id: str, operator: str, expected: Any):
    fn = __operators.get(operator)
    param = find_by_id(request['asset']['params'], param_id)
    assert fn(param['value'], expected)


def asset_params_value_equal(request: dict, param_id: str, expected: Any):
    asset_params_value(request, param_id, '==', expected)


def asset_params_value_not_equal(request: dict, param_id: str, expected: Any):
    asset_params_value(request, param_id, '!=', expected)


def asset_params_value_greater(request: dict, param_id: str, expected: Any):
    asset_params_value(request, param_id, '<', expected)


def asset_params_value_greater_or_equal(request: dict, param_id: str, expected: Any):
    asset_params_value(request, param_id, '<=', expected)


def asset_params_value_lesser(request: dict, param_id: str, expected: Any):
    asset_params_value(request, param_id, '>', expected)


def asset_params_value_lesser_or_equal(request: dict, param_id: str, expected: Any):
    asset_params_value(request, param_id, '>=', expected)


def asset_params_value_contains(request: dict, param_id: str, expected: Any):
    fn = __operators.get('in')
    param = find_by_id(request['asset']['params'], param_id)
    assert fn(expected, param['value'])


def asset_params_value_error(request: dict, param_id: str, operator: str, expected: Any):
    fn = __operators.get(operator)
    param = find_by_id(request['asset']['params'], param_id)
    assert fn(param['value_error'], expected)


def asset_params_value_equal_error(request: dict, param_id: str, expected: Any):
    asset_params_value_error(request, param_id, '==', expected)


def asset_params_value_not_equal_error(request: dict, param_id: str, expected: Any):
    asset_params_value_error(request, param_id, '!=', expected)


def asset_params_value_contains_error(request: dict, param_id: str, expected: Any):
    fn = __operators.get('in')
    param = find_by_id(request['asset']['params'], param_id)
    assert fn(expected, param['value_error'])


def tcr_status(request: dict, expected: str):
    assert request['configuration']['status'] == expected


def tcr_params_value(request: dict, param_id: str, operator: str, expected: Any):
    fn = __operators.get(operator)
    param = find_by_id(request['configuration']['params'], param_id)
    assert fn(param['value'], expected)


def tcr_params_value_equal(request: dict, param_id: str, expected: Any):
    tcr_params_value(request, param_id, '==', expected)


def tcr_params_value_not_equal(request: dict, param_id: str, expected: Any):
    tcr_params_value(request, param_id, '!=', expected)


def tcr_params_value_contains(request: dict, param_id: str, expected: Any):
    fn = __operators.get('in')
    param = find_by_id(request['configuration']['params'], param_id)
    assert fn(expected, param['value'])


def tcr_params_value_error(request: dict, param_id: str, operator: str, expected: Any):
    fn = __operators.get(operator)
    param = find_by_id(request['configuration']['params'], param_id)
    assert fn(param['value_error'], expected)


def tcr_params_value_equal_error(request: dict, param_id: str, expected: Any):
    tcr_params_value_error(request, param_id, '==', expected)


def tcr_params_value_not_equal_error(request: dict, param_id: str, expected: Any):
    tcr_params_value_error(request, param_id, '!=', expected)


def tcr_params_value_contains_error(request: dict, param_id: str, expected: Any):
    fn = __operators.get('in')
    param = find_by_id(request['configuration']['params'], param_id)
    assert fn(expected, param['value_error'])
