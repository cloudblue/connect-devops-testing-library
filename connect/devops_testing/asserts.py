import operator
import re
from typing import Any, Optional, Tuple

from connect.devops_testing.utils import find_by_id

ASSERT_FAIL = 'Assertion failed.'

__operators = {
    '==': operator.eq,
    '!=': operator.ne,
    'in': operator.contains,
    'match': lambda value, pattern: re.search(pattern, value),
}


def _prepare_assert_argument(param: dict, expected: Any) -> Tuple[Optional[Any], Any]:
    if param.get('type') == 'checkbox':
        return [k for k, v in param.get('structured_value', {}).items() if v], expected.split("|")
    else:
        return param.get('value', ''), expected


def request_status(request: dict, expected: str):
    assert request.get('status') == expected, f"Request status '{request.get('status')}' is not '{expected}'."


def request_reason(request: dict, expected: str):
    assert request.get('reason') == expected, f"Request reason '{request.get('reason')}' is not '{expected}'."


def request_note(request: dict, expected: str):
    assert request.get('note') == expected, f"Request note '{request.get('note')}' is not '{expected}'."


def task_response_status(task_response, expected: str):
    assert task_response.status == expected, f"Task Response status '{task_response.status}' is not '{expected}'."


def asset_status(request: dict, expected: str):
    value = request.get('asset', {}).get('status')
    assert value == expected, f"Asset status '{value}' is not '{expected}'."


def asset_param_value(request: dict, param_id: str, operator: str, expected: Any, msg: Optional[str] = None):
    fn = __operators.get(operator)
    param = find_by_id(request.get('asset', {}).get('params', []), param_id, {})
    value, expected = _prepare_assert_argument(param, expected)
    assert fn(value, expected), ASSERT_FAIL if msg is None else msg.format(
        param_id=param_id,
        value=value,
        expected=expected,
    )


def asset_param_value_equal(request: dict, param_id: str, expected: Any):
    msg = "{param_id} parameter value '{value}' is not equal to '{expected}'."
    asset_param_value(request, param_id, '==', expected, msg)


def asset_param_value_match(request: dict, param_id: str, pattern: str):
    msg = "{param_id} parameter value '{value}' does not match expression '{expected}'."
    asset_param_value(request, param_id, 'match', pattern, msg)


def asset_param_value_not_equal(request: dict, param_id: str, expected: Any):
    msg = "{param_id} parameter value '{value}' is equal to '{expected}'."
    asset_param_value(request, param_id, '!=', expected, msg)


def asset_param_value_contains(request: dict, param_id: str, expected: Any):
    msg = "{param_id} parameter value '{value}' does not contain '{expected}'."
    asset_param_value(request, param_id, 'in', expected, msg)


def asset_param_value_error(request: dict, param_id: str, operator: str, expected: Any, msg: Optional[str] = None):
    fn = __operators.get(operator)
    param = find_by_id(request.get('asset', {}).get('params', []), param_id, {})
    value = param.get('value_error', '')
    assert fn(value, expected), ASSERT_FAIL if msg is None else msg.format(
        param_id=param_id,
        value=value,
        expected=expected,
    )


def asset_param_value_error_equal(request: dict, param_id: str, expected: Any):
    msg = "{param_id} parameter value error '{value}' is not equal to '{expected}'."
    asset_param_value_error(request, param_id, '==', expected, msg)


def asset_param_value_error_not_equal(request: dict, param_id: str, expected: Any):
    msg = "{param_id} parameter value error '{value}' is equal to '{expected}'."
    asset_param_value_error(request, param_id, '!=', expected, msg)


def asset_param_value_error_contains(request: dict, param_id: str, expected: Any):
    msg = "{param_id} parameter value error '{value}' does not contain '{expected}'."
    asset_param_value_error(request, param_id, 'in', expected, msg)


def asset_param_value_error_match(request: dict, param_id: str, pattern: str):
    msg = "{param_id} parameter value error '{value}' does not match '{expected}'."
    asset_param_value_error(request, param_id, 'match', pattern, msg)


def tier_configuration_status(request: dict, expected: str):
    value = request.get('configuration', {}).get('status')
    assert value == expected, f"Tier Configuration status '{value}' is not '{expected}'."


def tier_configuration_param_value(
        request: dict,
        param_id: str,
        operator: str,
        expected: Any,
        msg: Optional[str] = None,
):
    fn = __operators.get(operator)
    param = find_by_id(
        request.get('params', request.get('configuration', {}).get('params', [])),
        param_id,
        {},
    )
    value, expected = _prepare_assert_argument(param, expected)
    assert fn(value, expected), ASSERT_FAIL if msg is None else msg.format(
        param_id=param_id,
        value=value,
        expected=expected,
    )


def tier_configuration_param_value_equal(request: dict, param_id: str, expected: Any):
    msg = "{param_id} parameter value '{value}' is not equal to '{expected}'."
    tier_configuration_param_value(request, param_id, '==', expected, msg)


def tier_configuration_param_value_not_equal(request: dict, param_id: str, expected: Any):
    msg = "{param_id} parameter value '{value}' is equal to '{expected}'."
    tier_configuration_param_value(request, param_id, '!=', expected, msg)


def tier_configuration_param_value_contains(request: dict, param_id: str, expected: Any):
    msg = "{param_id} parameter value '{value}' does not contain '{expected}'."
    tier_configuration_param_value(request, param_id, 'in', expected, msg)


def tier_configuration_param_value_match(request: dict, param_id: str, pattern: str):
    msg = "{param_id} parameter value '{value}' does not match expression '{expected}'."
    tier_configuration_param_value(request, param_id, 'match', pattern, msg)


def tier_configuration_param_value_error(
        request: dict,
        param_id: str,
        operator: str,
        expected: Any,
        msg: Optional[str] = None,
):
    fn = __operators.get(operator)
    param = find_by_id(
        request.get('params', request.get('configuration', {}).get('params', [])),
        param_id,
        {},
    )
    value = param.get('value_error', '')
    assert fn(value, expected), ASSERT_FAIL if msg is None else msg.format(
        param_id=param_id,
        value=value,
        expected=expected,
    )


def tier_configuration_param_value_error_equal(request: dict, param_id: str, expected: Any):
    msg = "{param_id} parameter value error '{value}' is not equal to '{expected}'."
    tier_configuration_param_value_error(request, param_id, '==', expected, msg)


def tier_configuration_param_value_error_not_equal(request: dict, param_id: str, expected: Any):
    msg = "{param_id} parameter value error '{value}' is equal to '{expected}'."
    tier_configuration_param_value_error(request, param_id, '!=', expected, msg)


def tier_configuration_param_value_error_contains(request: dict, param_id: str, expected: Any):
    msg = "{param_id} parameter value error '{value}' does not contain '{expected}'."
    tier_configuration_param_value_error(request, param_id, 'in', expected, msg)


def tier_configuration_param_value_error_match(request: dict, param_id: str, pattern: str):
    msg = "{param_id} parameter value error '{value}' does not match '{expected}'."
    tier_configuration_param_value_error(request, param_id, 'match', pattern, msg)
