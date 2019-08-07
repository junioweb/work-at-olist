from rest_framework import serializers

from .domain.bill import Bill


class BillSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        bill = Bill(obj)
        return {
            'subscriber': bill.subscriber,
            'period': bill.period,
            'total': 'R$ %.2f' % bill.total,
            'call_records': bill.call_records,
        }
