import copy

from datetime import time
from helpers import date_time_format

from bills.domain.price_rule import PriceRule
from bills.exceptions import CallDifferentPeriodsError, CallDifferentSubscribersError


class CallRecord:
    def __init__(self, call):
        self.rules = {
            'standard': PriceRule(start_time=time(hour=6, minute=0), end_time=time(hour=22, minute=0)),
            'reduced': PriceRule(name='Reduced', start_time=time(hour=22, minute=0),
                                 end_time=time(hour=6, minute=0), minute_charge=0.00)
        }
        self.call = call
        self.destination = call.start.destination
        self.start_date = call.start.timestamp.date()
        self.start_time = call.start.timestamp.time()
        self.duration = date_time_format.strfdelta(call.get_duration(), '{hours}h{minutes}m{seconds}s')

    @property
    def price(self):
        return self._calculate_tariff()

    def _calculate_tariff(self, call=None, partial_price=0.00, partial=False):
        if call is None:
            call = self.call

        if self._in_range_start_time_and_end_time(self.rules['standard'], call):
            return self._calculate_price_regular(self.rules['standard'], call, partial_price, partial)
        elif self._is_diff_dates_and_in_range_start_time_and_end_time(self.rules['reduced'], call):
            price, dt_partial = self._calculate_price_partial(self.rules['reduced'], call, partial_price, partial)
            call_copy = copy.deepcopy(call)
            call_copy.start.timestamp = dt_partial
            partial = True
            return self._calculate_tariff(call_copy, price, partial)
        elif self._in_range_start_time_and_end_time(self.rules['reduced'], call):
            return self._calculate_price_regular(self.rules['reduced'], call, partial_price, partial)
        elif self._in_range_start_time(self.rules['standard'], call):
            price, dt_partial = self._calculate_price_partial(self.rules['standard'], call, partial_price, partial)
            call_copy = copy.deepcopy(call)
            call_copy.start.timestamp = dt_partial
            partial = True
            return self._calculate_tariff(call_copy, price, partial)
        elif self._in_range_start_time(self.rules['reduced'], call):
            price, dt_partial = self._calculate_price_partial(self.rules['reduced'], call, partial_price, partial)
            call_copy = copy.deepcopy(call)
            call_copy.start.timestamp = dt_partial
            partial = True
            return self._calculate_tariff(call_copy, price, partial)

    def _in_range_start_time_and_end_time(self, rule, call):
        start_time = call.start.timestamp.time()
        end_time = call.end.timestamp.time()
        return rule.time_in_range(start_time) and rule.time_in_range(end_time)

    def _in_range_start_time(self, rule, call):
        start_time = call.start.timestamp.time()
        return rule.time_in_range(start_time)

    def _is_diff_dates_and_in_range_start_time_and_end_time(self, rule, call):
        start = call.start.timestamp
        end = call.end.timestamp
        return start.date() != end.date() and rule.time_in_range(start.time())

    def _calculate_price_regular(self, rule, call, partial_price, partial):
        duration = call.get_duration(in_minutes=True)
        return rule.calculate_price(duration, not partial) + partial_price

    def _calculate_price_partial(self, rule, call, partial_price, partial):
        call_copy = copy.deepcopy(call)
        if rule is self.rules['reduced']:
            day = call_copy.end.timestamp.day
            month = call_copy.end.timestamp.month
        else:
            day = call_copy.start.timestamp.day
            month = call_copy.start.timestamp.month
        partial_end = call_copy.end.timestamp.replace(day=day, month=month, hour=rule.end_time.hour,
                                                      minute=rule.end_time.minute, second=0)
        call_copy.end.timestamp = partial_end
        duration = call_copy.get_duration(in_minutes=True)
        price = rule.calculate_price(duration, not partial) + partial_price
        return price, partial_end


class Bill:
    def __init__(self, calls):
        self._calls = calls
        self._calls_is_valid()

    @property
    def subscriber(self):
        return self._calls[0].start.source

    @property
    def period(self):
        month = self._calls[0].end.timestamp.month
        year = self._calls[0].end.timestamp.year
        return '{}/{}'.format(month, year)

    @property
    def total(self):
        call_price = []
        for call in self._calls:
            call_record = CallRecord(call)
            call_price.append(call_record.price)
        return sum(call_price)

    @property
    def call_records(self):
        return [CallRecord(call) for call in self._calls]

    def _calls_is_valid(self):
        for call in self._calls:
            period = '{}/{}'.format(call.end.timestamp.month, call.end.timestamp.year)
            if period != self.period:
                raise CallDifferentPeriodsError()
            if call.start.source != self.subscriber:
                raise CallDifferentSubscribersError()
        return True
