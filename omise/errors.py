__all__ = [
    'AuthenticationFailureError',
    'NotFoundError',
    'UsedTokenError',
    'InvalidCardError',
    'InvalidCardTokenError',
    'MissingCardError',
    'InvalidChargeError',
    'FailedCaptureError',
    'FailedFraudCheckError',
    'FailedRefundError',
    'InvalidRecipientError',
]


def _get_error_for(type):
    """Returns a :type:`class` corresponding to :param:`type`.

    Used for getting an error from error code in JSON response.

    :type type: str
    :rtype: class
    """
    return {
        'authentication_failure': AuthenticationFailureError,
        'not_found': NotFoundError,
        'used_token': UsedTokenError,
        'invalid_card': InvalidCardError,
        'invalid_card_token': InvalidCardTokenError,
        'missing_card': MissingCardError,
        'invalid_charge': InvalidChargeError,
        'failed_capture': FailedCaptureError,
        'failed_fraud_check': FailedFraudCheckError,
        'failed_refund': FailedRefundError,
        'invalid_recipient': InvalidRecipientError,
    }.get(type)


def _raise_from_data(data):
    """Raise an error from API response.

    :type data: dict
    :rtype: None
    """
    if isinstance(data, dict):
        error = _get_error_for(data['code'])
        if not error:
            error = BaseError
        raise error(data['message'])
    raise BaseError('unknown error')


class BaseError(Exception):
    pass


class AuthenticationFailureError(BaseError):
    pass


class NotFoundError(BaseError):
    pass


class UsedTokenError(BaseError):
    pass


class InvalidCardError(BaseError):
    pass


class InvalidCardTokenError(BaseError):
    pass


class MissingCardError(BaseError):
    pass


class InvalidChargeError(BaseError):
    pass


class FailedCaptureError(BaseError):
    pass


class FailedFraudCheckError(BaseError):
    pass


class InvalidRecipientError(BaseError):
    pass


class FailedRefundError(BaseError):
    pass
