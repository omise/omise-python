# Omise Python Client

![Build Status](https://github.com/omise/omise-python/workflows/Python%20package/badge.svg?branch=master)
[![Python Versions](https://img.shields.io/pypi/pyversions/omise.svg?style=flat-square)](https://pypi.python.org/pypi/omise/)
[![PyPi Version](https://img.shields.io/pypi/v/omise.svg?style=flat-square)](https://pypi.python.org/pypi/omise/)

Please raise an issue or contact [support@omise.co](mailto:support@omise.co) if you have any question regarding this library and the functionality it provides.

## Installation

If you simply want to use Omise Python client in your application, you can install it using [pip](http://www.pip-installer.org/en/latest/index.html):

```
pip install omise
```

Or `easy_install` in case your system do not have pip installed:

```
easy_install omise
```

The Omise Python client officially supports the following Python versions:

* Python 2.7
* Python 3.6
* Python 3.7
* Python 3.8
* Python 3.9

Any versions not listed here _may_ work but they are not automatically tested.

## Usage

Please refer to examples in our [API documentation](https://www.omise.co/docs).
For basic usage, you can use the package in your application by importing `omise` and setting the secret key:

```python
import omise
omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
```

After the secret key is set, you can use all APIs which use secret key authentication.

To create a new credit card charge, use Omise.js to create a new token and run the following:

``` python
token_id = "tokn_test_no1t4tnemucod0e51mo" # see https://www.omise.co/tokens-api#create
charge = omise.Charge.create(
    amount=100000,
    currency="THB",
    card=token_id,
    return_uri="https://www.omise.co/example_return_uri",
)
# <Charge id='chrg_test_5ktrim62oiosnrc1r41' at 0x105d6bf28>
charge.status
# 'successful'
```

To create a new customer without any cards associated to the customer, run the following:

```python
customer = omise.Customer.create(
   description='John Doe',
   email='john.doe@example.com'
)
# <Customer id='cust_test_4xtrb759599jsxlhkrb' at 0x7ffab7136910>
```

Then to retrieve, update, and destroy that customer, run the following:

```python
customer = omise.Customer.retrieve('cust_test_4xtrb759599jsxlhkrb')
customer.description = 'John W. Doe'
customer.update()
# <Customer id='cust_test_4xtrb759599jsxlhkrb' at 0x7ffab7136910>
customer.destroy()
customer.destroyed
# True
```

In case of error (such as authentication failure, invalid card and others as listed in [errors](https://www.omise.co/api-errors/) section in the documentation), the error of a subclass `omise.errors.BaseError` will be raised.
Your application code should handle these errors appropriately.

### API version

In case you want to enforce API version the application use, you can specify it by setting `api_version`.
The version specified by this setting will override the version setting in your account.
This is useful if you have multiple environments with different API versions (e.g. development on the latest but production on the older version).

```python
import omise
omise.api_version = '2019-05-29'
```

It is highly recommended to set this version to the current version you're using.

## Contributing

The Omise Python client uses `tox` and [Docker](https://docs.docker.com/) for testing.
All changes must be tested against all supported Python versions.
You can run tests using the following instructions:

1. Install [Docker](https://docs.docker.com/)
2. Run `docker run -it -v $(pwd):/app --rm $(docker build -q .)`

This command builds a Docker image using the [Dockerfile](Dockerfile), mounts the current directory to the container's `/app` directory, and runs the default entrypoint for the image: `/app/run-tox.sh`.

After you've made your changes and run the tests, please open a [Pull Request](https://github.com/omise/omise-python/pulls).

## License

See [LICENSE.txt](https://github.com/omise/omise-python/blob/master/LICENSE.txt)
