from rest_framework import serializers


class CallRecordSerializer(serializers.Serializer):
    destination = serializers.CharField(min_length=10, max_length=11, read_only=True)
    start_date = serializers.DateField(read_only=True)
    start_time = serializers.TimeField(read_only=True)
    duration = serializers.CharField(read_only=True)
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return 'R$ %.2f' % obj.price


class BillSerializer(serializers.Serializer):
    subscriber = serializers.CharField(min_length=10, max_length=11, read_only=True)
    period = serializers.CharField(min_length=6, max_length=7, read_only=True)
    total = serializers.SerializerMethodField()
    call_records = CallRecordSerializer(many=True)

    def get_total(self, obj):
        return 'R$ %.2f' % obj.total
