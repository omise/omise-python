## [0.7.0] - 2017-10-17

This version adds support for Receipt API, and Source API.

* [Added] Add Receipt API.
* [Added] Add Source API.

## [0.6.0] - 2017-06-12

This version adds support for Forex API, and Search API, Schedule API and Occurrence API and drop and add support Python new version.

* [Added] Add Forex API.
* [Added] Add Search API.
* [Added] Add Schedule API.
* [Added] Add Occurrence API.
* [Changed] Drop support Python 2.6 and add support Python 3.6.

## [0.5.0] - 2017-03-28

This version adds support for link API.

* [Added] Add Link API support.

## [0.4.1] - 2016-12-09

This version fixes compatibility with [Requests](https://github.com/kennethreitz/requests/) library version 2.12.1 and above.

* [Fixed] Compatibility with Requests 2.12.1.

## [0.4.0] - 2016-11-10

This version adds support for event and reversal API as well as dropping support for Python 3.1 and Python 3.2 in favor for Ptyhon 3.4 and Python 3.5.

* [Added] Add Reversal API support.
* [Added] Add Event API support.
* [Added] Official support for Python 3.4.
* [Added] Official support for Python 3.5.
* [Removed] Official support for Python 3.1.
* [Removed] Official support for Python 3.2.

## [0.3.0] - 2015-11-13

This version adds support for configuring Omise API version via `omise.api_version` settings. If this version is set, it will be used instead of the one setting in your Omise account.

* [Added] Add API versioning support.

## [0.2.1] - 2015-08-03

This version is a maintenance release which updates the bundled CA certificate file to latest version. The old CA certificate will no longer be able to connect with Omise API by August 18th, 2015. There is no added APIs or behavior changes in this release.

- [Changed] Update the bundled CA certificate.

## [0.2.0] - 2015-06-18

This version adds support for dispute and recipient API as well as change the way requests are made to the server. Internally, the library now uses `application/json` as POST request body instead of `x-www-form-urlencoded`. The change should result a more consistent requests (as objects now serialized and sent as it is, instead of doing extra data transformation.)

- [Added] Add Dispute API support.
- [Added] Add Recipient API support.
- [Changed] Use JSON for POST body instead of URL-encoded form.

## [0.1.0] - 2015-01-26

This version is an initial public release which supported all basic API features existed on the date of release.

- [Added] Add Account API support.
- [Added] Add Balance API support.
- [Added] Add Card API support.
- [Added] Add Charge API support.
- [Added] Add Customer API support.
- [Added] Add Refund API support.
- [Added] Add Token API support.
- [Added] Add Transaction API support.
- [Added] Add Transfer API support.
