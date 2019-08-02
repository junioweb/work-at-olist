from rest_framework.exceptions import APIException


class CallStartMissingError(APIException):
    status_code = 422
    default_detail = 'Not allowed to create a end call without a start call'
    default_code = 'call_start_missing_error'


class TimestampLessThanCallStartTimestampError(APIException):
    status_code = 422
    default_detail = 'End call timestamp can\'t be less than the start call timestamp'
    default_code = 'timestamp_less_than_call_start_timestamp_error'


class TimestampGreaterThanCallEndTimestampError(APIException):
    status_code = 422
    default_detail = 'Start call timestamp can\'t be greater than the end call timestamp'
    default_code = 'timestamp_greater_than_call_end_timestamp_error'


class TypeCallMissingError(APIException):
    status_code = 400
    default_detail = 'Not allowed to create or update a call record without a field type'
    default_code = 'type_call_missing_error'


class RecordsMissingError(APIException):
    status_code = 400
    default_detail = 'Not allowed to create or update a call without a list field records'
    default_code = 'records_missing_error'


class EmptyRecordsError(APIException):
    status_code = 400
    default_detail = 'Not allowed to create or update a call with empty records'
    default_code = 'empty_records_error'
