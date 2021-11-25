# Connect DevOps Testing Library

![pyversions](https://img.shields.io/pypi/pyversions/connect-devops-testing-library.svg) [![PyPi Status](https://img.shields.io/pypi/v/connect-devops-testing-library.svg)](https://pypi.org/project/connect-devops-testing-library/) [![Build Status](https://github.com/cloudblue/connect-devops-testing-library/actions/workflows/test.yml/badge.svg)](https://github.com/cloudblue/connect-devops-testing-library/actions/workflows/test.yml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=connect-devops-testing-library&metric=alert_status)](https://sonarcloud.io/dashboard?id=connect-devops-testing-library)

Testing library to ease Connect EaaS Processors development.

## Install

`Connect DevOps Testing Library` can be installed
from [pypi.org](https://pypi.org/project/connect-devops-testing-library/) using pip:

```bash
$ pip install connect-devops-testing-library
```

## Usage

DevOps Testing Library has a small request builder to ease the manipulation of the connect requests during testing:

````python
from connect.devops_testing import fixtures
import os

template = os.path.dirname(__file__) + '/request.json'

request = (fixtures.make_request_builder(template)
           .with_type('purchase')
           .with_asset_product('PRD-000-000-000', 'Product Name')
           .with_asset_configuration_param('SOME_ASSET_CFG__PARAM_ID_A', 'some_cfg_value_a')
           .with_asset_param('SOME_ASSET_PARAM_ID_001', 'some_value_001')
           .with_asset_param('SOME_ASSET_PARAM_ID_002', 'some_value_002')
           .build())
````

DevOps Testing Library also has several built-in assert functions that can be easily used to evaluate a connect request
response:

```python
from connect.devops_testing import asserts

asserts.request_status(request, 'approved')
asserts.asset_status(request, 'active')
asserts.asset_param_value_not_equal(request, 'SOME_ASSET_PARAM_ID_001', 'some_expected_value')
```

Using these two features you can easily create a small test to check a purchase request of your processor:

```python
from connect.devops_testing import fixtures, asserts
from my_ext.extension import MyExtension
import os


def test_should_approve_request(mocked_connect_client, mocked_service_client, logger, eaas_config):
    template = os.path.dirname(__file__) + '/request.json'

    # prepare the request.
    request = (fixtures.make_request_builder(template)
               .with_type('purchase')
               .with_status('pending')
               .with_asset_param('subscription_id', '')
               .build())

    # instantiate and execute the extension for the given request.
    extension = MyExtension(mocked_connect_client, logger, eaas_config)
    result = extension.process_asset_adjustment_request(request)

    # evaluate the task result and request.
    asserts.task_response_status(result, 'success')
    asserts.request_status(request, 'approved')
    asserts.asset_status(request, 'active')
    asserts.asset_param_value(request, 'subscription_id', '==', 'ID:123456789')
```

Additionally, you may want to create real end-to-end test calling Connect and evaluating the processed request, for this
you should use the built-in request dispatcher. The dispatcher will take automatically the required credentials from the
environment variables in `CONNECT_API_KEY` and `CONNECT_API_URL`. Alternatively, you can pass explicitly the credentials
to the `make_request_dispatcher(api_key=XXX, api_url=YYY)` function. Let's see example:

```python
from connect.devops_testing import asserts, fixtures
import os


def test_should_approve_purchase_request_successfully():
    template = os.path.dirname(__file__) + '/request.json'

    # prepare the request.
    request = (fixtures.make_request_builder(template)
               .with_type('purchase')
               .with_status('pending')
               .with_asset_param('subscription_id', '')
               .build())

    # dispatch the request to connect and wait some time so the 
    # processor can process the request.
    request = (fixtures.make_request_dispatcher()
               .provision_request(request, 10, 20))

    # evaluate the processed request.
    asserts.request_status(request, 'approved')
    asserts.asset_status(request, 'active')
    asserts.asset_param_value(request, 'subscription_id', '==', 'ID:123456789')
```

Once the request is dispatched the Dispatcher will reload the request again every `10` seconds a maximum of `20`
attempts. If the request has not been processed the asserts may fail. The wait time between request reload can be
configured directly in the `.provision_request(timeout=10, max_attempt=20)` method call.

Obviously, some Connect processors may take a lot of time to process a request, for those type of processors this kind
of end-to-end test is not suitable.

### Behavior Driven Development

Finally, the DevOps Testing Library also allows you to easily use Behave! BDD tool for you test. You just need to set
the following code in your `features/environment.py` file

```python
from behave import use_fixture

# import the built-in steps for e2e testing. 
from connect.devops_testing.bdd import steps
from connect.devops_testing.bdd.fixtures import (
    use_connect_request_dispatcher,
    use_connect_request_builder,
    use_connect_request_store,
)


def before_all(context):
    # attach the request dispatcher to the behave context.
    use_fixture(
        fixture_func=use_connect_request_dispatcher,
        context=context,
    )
    # attach the request builder to the behave context.
    use_fixture(
        fixture_func=use_connect_request_builder,
        context=context,
    )


def before_feature(context, feature):
    # reset the request store for each feature
    use_fixture(
        fixture_func=use_connect_request_store,
        context=context,
        reset=True
    )

```

It's time to define the feature file in `features/purchase.feature`:

```gherkin
Feature: Purchase a new subscription.

  Scenario: Customer buys a subscription.
    Given a new valid email address
    When subscription request is processed
    Then the subscription id is provided
```

Now let's define the steps in `features/steps/purchase.py` file

```python
from behave import given, then
from connect.devops_testing import asserts
import os


@given("a new valid email address")
def step_impl(context):
    template = os.path.dirname(__file__) + '/request.json'

    context.request = (context.builder
                       .from_file(template)
                       .with_asset_param('CUSTOMER_EMAIL_ADDRESS', 'vincent.vega@gmail.com'))


@then("the subscription id is provided")
def step_impl(context):
    asserts.request_status(context.request, 'approved')
    asserts.asset_status(context.request, 'active')
    asserts.asset_param_value_not_equal(context.request, 'CUSTOMER_EMAIL_ADDRESS', '')
```

The `@step("subscription request is processed")` is provided by the DevOps Testing Library.

Available BDD steps:

| Step | Description |
| ------------- | ------------- |
| `request is processed`  | Process the request into Connect Platform. |
| `subscription request is processed`  | Alias of `request is processed`. |
| `tier configuration request is processed`  | Alias of `request is processed`. |
| `tier config request`  | Loads a tier configuration request template. |
| `asset request`  | Loads an asset request template. |
| `request with id "{request_id}"`  | Sets the request id. |
| `request with status "{request_status}"`  | Set the request status. |
| `request with configuration account "{account_id}"`  | Set the request tier configuration account id. |
| `request with product "{product_id}"`  | Set the request product id. |
| `request with marketplace "{marketplace_id}"`  | Set the request marketplace id. |
| `request with reseller level "{level}"`  | Set the request tier configuration reseller level. |
| `request with parameter "{parameter}" with value "{value}"`  | Set a request parameter value by parameter id. |
| `request with parameter "{parameter}" value "{values}" checked`  | Check a request checkbox parameter values by id. |
| `request with parameter "{parameter}" value "{values}" not checked`  | Uncheck a request checkbox parameter values by id. |
| `request with parameter "{parameter}" without value`  | Unset the request parameter value by id. |
| `request with parameter "{parameter}" with value error "{value}"`  | Set the request parameter value error by id. |
| `request with parameter "{parameter}" without value error`  | Unset the request parameter value error. |
| `request parameter "{parameter}" value is "{value}"`  | Assert that the value of the given parameter by id is the expected one. |
| `request parameter "{parameter}" value contains "{value}"`  | Assert that the value of the given parameter by id contains the expected value. |
| `request parameter "{parameter}" value match "{pattern}"`  | Assert that the value of the given parameter by id match the expected regex expression. |
| `request parameter "{parameter}" value error is "{value_error}"`  | Assert that the value error of the given parameter by id the expected one.  |
| `request parameter "{parameter}" value error contains "{value_error}"`  | Assert that the value error of the given parameter by id contains the expected value. |
| `request parameter "{parameter}" value error match "{pattern}"`  | Assert that the value error of the given parameter by id match the expected regex expression. |
| `request status is "{request_status}"`  | Assert that the status of the request is the expected one. |

## License

`Connect DevOps Testing Library` is released under
the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).