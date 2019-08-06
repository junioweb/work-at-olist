import datetime


class PriceRule:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Standard')
        self.start_time = kwargs.get('start_time', datetime.time(hour=0, minute=0))
        self.end_time = kwargs.get('end_time', datetime.time(hour=23, minute=59))
        self.standing_charge = kwargs.get('standing_charge', 0.36)
        self.minute_charge = kwargs.get('minute_charge', 0.09)
        self.has_plus_day = kwargs.get('has_plus_day', False)

    def calculate_price(self, duration, with_connection=True):
        price = duration * self.minute_charge
        if with_connection:
            return price + self.standing_charge
        else:
            return price
