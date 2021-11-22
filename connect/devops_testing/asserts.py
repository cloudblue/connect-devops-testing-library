import operator
import re
from typing import Any, Optional, Tuple

from connect.devops_testing.utils import find_by_id

__operators = {
    '==': operator.eq,
    '!=': operator.ne,
    'in': operator.contains,
    'match': lambda value, pattern: re.search(pattern, value),
}


def _prepare_assert_argument(param: dict, expected: Any) -> Tuple[Optional[Any], Any]:
    if param.get('type') == 'checkbox':
        return [k for k, v in param.get('structured_value').items() if v], expected.split("|")
    else:
        return param.get('value'), expected


def request_status(request: dict, expected: str):
    assert request.get('status') == expected


def request_reason(request: dict, expected: str):
    assert request.get('reason') == expected


def request_note(request: dict, expected: str):
    assert request.get('note') == expected


def task_response_status(task_response, expected: str):
    assert task_response.status == expected


def asset_status(request: dict, expected: str):
    assert request.get('asset', {}).get('status') == expected


def asset_param_value(request: dict, param_id: str, operator: str, expected: Any):
    fn = __operators.get(operator)
    param = find_by_id(request.get('asset', {}).get('params', []), param_id, {})

    assert fn(*_prepare_assert_argument(param, expected))


def asset_param_value_equal(request: dict, param_id: str, expected: Any):
    asset_param_value(request, param_id, '==', expected)


def asset_param_value_match(request: dict, param_id: str, pattern: str):
    asset_param_value(request, param_id, 'match', pattern)


def asset_param_value_not_equal(request: dict, param_id: str, expected: Any):
    asset_param_value(request, param_id, '!=', expected)


def asset_param_value_contains(request: dict, param_id: str, expected: Any):
    asset_param_value(request, param_id, 'in', expected)


def asset_param_value_error(request: dict, param_id: str, operator: str, expected: Any):
    fn = __operators.get(operator)
    param = find_by_id(request.get('asset', {}).get('params', []), param_id, {})
    assert fn(param.get('value_error'), expected)


def asset_param_value_error_equal(request: dict, param_id: str, expected: Any):
    asset_param_value_error(request, param_id, '==', expected)


def asset_param_value_error_not_equal(request: dict, param_id: str, expected: Any):
    asset_param_value_error(request, param_id, '!=', expected)


def asset_param_value_error_contains(request: dict, param_id: str, expected: Any):
    asset_param_value_error(request, param_id, 'in', expected)


def asset_param_value_error_match(request: dict, param_id: str, pattern: str):
    asset_param_value_error(request, param_id, 'match', pattern)


def tier_configuration_status(request: dict, expected: str):
    assert request.get('configuration', {}).get('status') == expected


def tier_configuration_param_value(request: dict, param_id: str, operator: str, expected: Any):
    fn = __operators.get(operator)
    param = find_by_id(
        request.get('params', request.get('configuration', {}).get('params', [])),
        param_id,
        {},
    )
    assert fn(*_prepare_assert_argument(param, expected))


def tier_configuration_param_value_equal(request: dict, param_id: str, expected: Any):
    tier_configuration_param_value(request, param_id, '==', expected)


def tier_configuration_param_value_not_equal(request: dict, param_id: str, expected: Any):
    tier_configuration_param_value(request, param_id, '!=', expected)


def tier_configuration_param_value_contains(request: dict, param_id: str, expected: Any):
    tier_configuration_param_value(request, param_id, 'in', expected)


def tier_configuration_param_value_match(request: dict, param_id: str, pattern: str):
    tier_configuration_param_value(request, param_id, 'match', pattern)


def tier_configuration_param_value_error(request: dict, param_id: str, operator: str, expected: Any):
    fn = __operators.get(operator)
    param = find_by_id(
        request.get('params', request.get('configuration', {}).get('params', [])),
        param_id,
        {},
    )
    assert fn(param.get('value_error'), expected)


def tier_configuration_param_value_error_equal(request: dict, param_id: str, expected: Any):
    tier_configuration_param_value_error(request, param_id, '==', expected)


def tier_configuration_param_value_error_not_equal(request: dict, param_id: str, expected: Any):
    tier_configuration_param_value_error(request, param_id, '!=', expected)


def tier_configuration_param_value_error_contains(request: dict, param_id: str, expected: Any):
    tier_configuration_param_value_error(request, param_id, 'in', expected)


def tier_configuration_param_value_error_match(request: dict, param_id: str, pattern: str):
    tier_configuration_param_value_error(request, param_id, 'match', pattern)
