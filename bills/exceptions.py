from rest_framework.exceptions import APIException


class CallDifferentPeriodsError(APIException):
    status_code = 422
    default_detail = 'Not allowed to create bill instance with call different periods'
    default_code = 'call_different_periods_error'


class CallDifferentSubscribersError(APIException):
    status_code = 422
    default_detail = 'Not allowed to create bill instance with call different subscribers'
    default_code = 'call_different_subscribers_error'


class SubscriberNotPassedError(APIException):
    status_code = 422
    default_detail = 'Not allowed to get bills when subscriber not informed'
    default_code = 'subscriber_not_passed_error'
