from django.core.exceptions import ValidationError


class CallStartMissingError(ValidationError):
    def __init__(self, message=None, code=None, params=None):
        if not message:
            message = 'Not allowed to create a end call without a start call'
        super().__init__(message, code, params)


class TimestampLessThanCallStartTimestampError(ValidationError):
    def __init__(self, message=None, code=None, params=None):
        if not message:
            message = 'End call timestamp can\'t be less than the start call timestamp'
        super().__init__(message, code, params)


class TimestampGreaterThanCallEndTimestampError(ValidationError):
    def __init__(self, message=None, code=None, params=None):
        if not message:
            message = 'Start call timestamp can\'t be greater than the end call timestamp'
        super().__init__(message, code, params)


class TypeCallMissingError(ValidationError):
    def __init__(self, message=None, code=None, params=None):
        if not message:
            message = 'Not allowed to create or update a call record without a field type'
        super().__init__(message, code, params)


class RecordsMissingError(ValidationError):
    def __init__(self, message=None, code=None, params=None):
        if not message:
            message = 'Not allowed to create or update a call without a list field records'
        super().__init__(message, code, params)


class EmptyRecordsError(ValidationError):
    def __init__(self, message=None, code=None, params=None):
        if not message:
            message = 'Not allowed to create or update a call with empty records'
        super().__init__(message, code, params)
