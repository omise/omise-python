# Omise Python Client

[![Build Status](https://img.shields.io/travis/omise/omise-python.svg?style=flat-square)](https://travis-ci.org/omise/omise-python)
[![Python Versions](https://img.shields.io/pypi/pyversions/omise.svg?style=flat-square)](https://pypi.python.org/pypi/omise/)
[![PyPi Version](https://img.shields.io/pypi/v/omise.svg?style=flat-square)](https://pypi.python.org/pypi/omise/)
[![](https://img.shields.io/badge/discourse-forum-1a53f0.svg?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAAAXNSR0IArs4c6QAAAAlwSFlzAAALEwAACxMBAJqcGAAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAAqlJREFUKBU9UVtLVFEU%2FvY%2B27mPtxl1dG7HbNRx0rwgFhJBPohBL9JTZfRQ0YO9RU%2FVL6iHCIKelaCXqIewl4gEBbEyxSGxzKkR8TbemmbmnDlzVvsYtOHbey1Y317fWh8DwCVMCfSHww3ElCs7CjuzbOcNIaEo9SbtlDRjZiNPY%2BvrqSWrTh7l3yPvrmh0KBZW59HcREjEqcGpElAuESRxopU648dTwfrIyH%2BCFXSH1cFgJLqHlma6443SG0CfqYY2NZjQnkV8eiMgP6ijjnizHglErlocdl5VA0mT3v102dseL2W14cYM99%2B9XGY%2FlQArd8Mo6JhbSJUePHytvf2UdnW0qen93cKQ4nWXX1%2FyOkZufsuZN0L7PPzkthDDZ4FQLajSA6XWR8HWIK861sCfj68ggGwl83mzfMclBmAQ%2BktrqBu9wOhcD%2BB0ErSiFFyEkdcYhKD27mal9%2F5FY36b4BB%2FTvO8XdQhlUe11F3WG2fc7QLlC8wai3MGGQCGDkcZQyymCqAPSmati3s45ygWseeqADwuWS%2F3wGS5hClDMMstxvJFHQuGU26yHsY6iHtL0sIaOyZzB9hZz0hHZW71kySSl6LIJlSgj5s5LO6VG53aFgpOfOFCyoFmYsOS5HZIaxVwKYsLSbJJn2kfU%2BlNdms5WMLqQRklX0FX26eFRnKYwzX0XRsgR0uUrWxplM7oqPIq8r8cZrdLNLqaABayxZMTTx2HVfglbP4xkcvqZEMNfmglevRi1ny5mGfJfTuQiBEq%2FMBvG0NqDh2TY47sbtJAuO%2Fe9%2Fn3STRFosm2WIxsFSFrFUfwHb11JNBNcaZSp8yb%2FEhHW3suWRNZRzDGvxb0oifk5lmnX2V2J2dEJkX1Q0baZ1MvYXPXHvhAga7x9PTEyj8a%2BF%2BXbxiTn78bSQAAAABJRU5ErkJggg%3D%3D)](https://forum.omise.co)

Please pop onto our [community forum](https://forum.omise.co) or contact
[support@omise.co](mailto:support@omise.co) if you have any question regarding this
library and the functionality it provides.

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

See [LICENSE.txt](https://github.com/omise/omise-python/blob/master/LICENSE.txt)
