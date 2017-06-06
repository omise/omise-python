# Omise Python Client

[![Build Status](https://img.shields.io/travis/omise/omise-python.svg?style=flat-square)](https://travis-ci.org/omise/omise-python)
[![Python Versions](https://img.shields.io/pypi/pyversions/omise.svg?style=flat-square)](https://pypi.python.org/pypi/omise/)
[![PyPi Version](https://img.shields.io/pypi/v/omise.svg?style=flat-square)](https://pypi.python.org/pypi/omise/)

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
* Python 3.3
* Python 3.4
* Python 3.5
* Python 3.6

Any versions not listed here _may_ work but they are not automatically tested.

## Usage

Please refer to an example in [API documentation](https://docs.omise.co/) or the [help](https://docs.python.org/2/library/functions.html#help) function for documentation. For basic usage, you can use the module in your application by importing the `omise` module and set the secret key and public key:

```python
>>> import omise
>>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
>>> omise.api_public = 'pkey_test_4xs8breq32civvobx15'
```

After both keys are set, you can now use all the APIs. For example, to create a new customer without any cards associated to the customer:

```python
>>> customer = omise.Customer.create(
>>>    description='John Doe',
>>>    email='john.doe@example.com'
>>> )
<Customer id='cust_test_4xtrb759599jsxlhkrb' at 0x7ffab7136910>
```

Then to retrieve, update and destroy that customer:

```python
>>> customer = omise.Customer.retrieve('cust_test_4xtrb759599jsxlhkrb')
>>> customer.description = 'John W. Doe'
>>> customer.update()
<Customer id='cust_test_4xtrb759599jsxlhkrb' at 0x7ffab7136910>
>>> customer.destroy()
>>> customer.destroyed
True
```

In case of any errors (such as authentication failure, invalid card and others as listed in [errors](https://docs.omise.co/api/errors/) section in the documentation), the error of a subclass `omise.errors.BaseError` will be raise. The application code must be handling these errors as appropriate.

### API version

In case you want to enforce API version the application use, you can specify it by setting `api_version`. The version specified by this settings will override the version setting in your account. This is useful if you have multiple environments with different API versions (e.g. development on the latest but production on the older version).

```python
>>> import omise
>>> omise.api_version = '2014-07-27'
```

It is highly recommended to set this version to the current version you're using.

## Contributing

The Omise Python client uses [Vagrant](https://www.vagrantup.com/) for development environment provisioning and require all changes to be tested against all supported Python versions. You can bootstrap the environment with the following instructions:

1. Install [Vagrant](https://www.vagrantup.com/) with [provider](https://docs.vagrantup.com/v2/providers/index.html) of your choice (e.g. [VirtualBox](https://www.virtualbox.org/))
2. Run `vagrant up` and read Vagrant's [Getting Started](https://docs.vagrantup.com/v2/getting-started/index.html) while waiting.

After the box is up and running, you can now SSH to the server and run [tox](http://tox.readthedocs.org/en/latest/) to test against all supported Python versions:

1. Run `vagrant ssh` to SSH into the provisioned box.
2. Run `cd /vagrant` to navigate to working directory.
3. Run `tox` to run tests against all supported Python versions.

Any changes made locally to the source code will be automatically updated to the box. After you've done with the changes, please open a [Pull Request](https://github.com/omise/omise-python/pulls).

## License

See LICENSE.txt
