import operator
import re
from typing import Any, Optional, Tuple

from connect.devops_testing.utils import find_by_id

ASSERT_FAIL = 'Assertion failed.'

_MSG_PARAM_NOT_EQUAL = "{param_id} parameter value '{value}' is not equal to '{expected}'."
_MSG_PARAM_IS_EQUAL = "{param_id} parameter value '{value}' is equal to '{expected}'."
_MSG_PARAM_NOT_MATCH = "{param_id} parameter value '{value}' does not match expression '{expected}'."
_MSG_PARAM_NOT_CONTAIN = "{param_id} parameter value '{value}' does not contain '{expected}'."
_MSG_PARAM_ERROR_NOT_EQUAL = "{param_id} parameter value error '{value}' is not equal to '{expected}'."
_MSG_PARAM_ERROR_IS_EQUAL = "{param_id} parameter value error '{value}' is equal to '{expected}'."
_MSG_PARAM_ERROR_NOT_MATCH = "{param_id} parameter value error '{value}' does not match '{expected}'."
_MSG_PARAM_ERROR_NOT_CONTAIN = "{param_id} parameter value error '{value}' does not contain '{expected}'."

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


def request_id(request: dict, expected: str):
    assert request.get('id') == expected, f"Request id '{request.get('id')}' is not '{expected}'"


def request_status(request: dict, expected: str):
    assert request.get('status') == expected, f"Request status '{request.get('status')}' is not '{expected}'."


def request_type(request: dict, expected: str):
    assert request.get('type') == expected, f"Request type '{request.get('type')}' is not '{expected}'."


def request_reason(request: dict, expected: str):
    assert request.get('reason') == expected, f"Request reason '{request.get('reason')}' is not '{expected}'."


def request_note(request: dict, expected: str):
    assert request.get('note') == expected, f"Request note '{request.get('note')}' is not '{expected}'."


def request_param_value(request: dict, param_id: str, operator: str, expected: Any, msg: Optional[str] = None):
    fn = __operators.get(operator)
    param = find_by_id(request.get('params', []), param_id, {})
    value, expected = _prepare_assert_argument(param, expected)
    assert fn(value, expected), ASSERT_FAIL if msg is None else msg.format(
        param_id=param_id,
        value=value,
        expected=expected,
    )


def request_param_value_equal(request: dict, param_id: str, expected: Any):
    request_param_value(request, param_id, '==', expected, _MSG_PARAM_NOT_EQUAL)


def request_param_value_match(request: dict, param_id: str, pattern: str):
    request_param_value(request, param_id, 'match', pattern, _MSG_PARAM_NOT_MATCH)


def request_param_value_not_equal(request: dict, param_id: str, expected: Any):
    request_param_value(request, param_id, '!=', expected, _MSG_PARAM_IS_EQUAL)


def request_param_value_contains(request: dict, param_id: str, expected: Any):
    request_param_value(request, param_id, 'in', expected, _MSG_PARAM_NOT_CONTAIN)


def request_param_value_error(request: dict, param_id: str, operator: str, expected: Any, msg: Optional[str] = None):
    fn = __operators.get(operator)
    param = find_by_id(request.get('params', []), param_id, {})
    value = param.get('value_error', '')
    assert fn(value, expected), ASSERT_FAIL if msg is None else msg.format(
        param_id=param_id,
        value=value,
        expected=expected,
    )


def request_param_value_error_equal(request: dict, param_id: str, expected: Any):
    request_param_value_error(request, param_id, '==', expected, _MSG_PARAM_ERROR_NOT_EQUAL)


def request_param_value_error_not_equal(request: dict, param_id: str, expected: Any):
    request_param_value_error(request, param_id, '!=', expected, _MSG_PARAM_ERROR_IS_EQUAL)


def request_param_value_error_contains(request: dict, param_id: str, expected: Any):
    request_param_value_error(request, param_id, 'in', expected, _MSG_PARAM_ERROR_NOT_CONTAIN)


def request_param_value_error_match(request: dict, param_id: str, pattern: str):
    request_param_value_error(request, param_id, 'match', pattern, _MSG_PARAM_ERROR_NOT_MATCH)


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
    asset_param_value(request, param_id, '==', expected, _MSG_PARAM_NOT_EQUAL)


def asset_param_value_match(request: dict, param_id: str, pattern: str):
    asset_param_value(request, param_id, 'match', pattern, _MSG_PARAM_NOT_MATCH)


def asset_param_value_not_equal(request: dict, param_id: str, expected: Any):
    asset_param_value(request, param_id, '!=', expected, _MSG_PARAM_IS_EQUAL)


def asset_param_value_contains(request: dict, param_id: str, expected: Any):
    asset_param_value(request, param_id, 'in', expected, _MSG_PARAM_NOT_CONTAIN)


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
    asset_param_value_error(request, param_id, '==', expected, _MSG_PARAM_ERROR_NOT_EQUAL)


def asset_param_value_error_not_equal(request: dict, param_id: str, expected: Any):
    asset_param_value_error(request, param_id, '!=', expected, _MSG_PARAM_ERROR_IS_EQUAL)


def asset_param_value_error_contains(request: dict, param_id: str, expected: Any):
    asset_param_value_error(request, param_id, 'in', expected, _MSG_PARAM_ERROR_NOT_CONTAIN)


def asset_param_value_error_match(request: dict, param_id: str, pattern: str):
    asset_param_value_error(request, param_id, 'match', pattern, _MSG_PARAM_ERROR_NOT_MATCH)


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
    param = find_by_id(request.get('configuration', {}).get('params', []), param_id, {})
    value, expected = _prepare_assert_argument(param, expected)
    assert fn(value, expected), ASSERT_FAIL if msg is None else msg.format(
        param_id=param_id,
        value=value,
        expected=expected,
    )


def tier_configuration_param_value_equal(request: dict, param_id: str, expected: Any):
    tier_configuration_param_value(request, param_id, '==', expected, _MSG_PARAM_NOT_EQUAL)


def tier_configuration_param_value_not_equal(request: dict, param_id: str, expected: Any):
    tier_configuration_param_value(request, param_id, '!=', expected, _MSG_PARAM_IS_EQUAL)


def tier_configuration_param_value_contains(request: dict, param_id: str, expected: Any):
    tier_configuration_param_value(request, param_id, 'in', expected, _MSG_PARAM_NOT_CONTAIN)


def tier_configuration_param_value_match(request: dict, param_id: str, pattern: str):
    tier_configuration_param_value(request, param_id, 'match', pattern, _MSG_PARAM_NOT_MATCH)


def tier_configuration_param_value_error(
        request: dict,
        param_id: str,
        operator: str,
        expected: Any,
        msg: Optional[str] = None,
):
    fn = __operators.get(operator)
    param = find_by_id(request.get('configuration', {}).get('params', []), param_id, {})
    value = param.get('value_error', '')
    assert fn(value, expected), ASSERT_FAIL if msg is None else msg.format(
        param_id=param_id,
        value=value,
        expected=expected,
    )


def tier_configuration_param_value_error_equal(request: dict, param_id: str, expected: Any):
    tier_configuration_param_value_error(request, param_id, '==', expected, _MSG_PARAM_ERROR_NOT_EQUAL)


def tier_configuration_param_value_error_not_equal(request: dict, param_id: str, expected: Any):
    tier_configuration_param_value_error(request, param_id, '!=', expected, _MSG_PARAM_ERROR_IS_EQUAL)


def tier_configuration_param_value_error_contains(request: dict, param_id: str, expected: Any):
    tier_configuration_param_value_error(request, param_id, 'in', expected, _MSG_PARAM_ERROR_NOT_CONTAIN)


def tier_configuration_param_value_error_match(request: dict, param_id: str, pattern: str):
    tier_configuration_param_value_error(request, param_id, 'match', pattern, _MSG_PARAM_ERROR_NOT_MATCH)
