import datetime

from rest_framework import serializers

from calls.domain.call import Call, CallEnd, CallStart


class CallStartSerializer(serializers.ModelSerializer):
    call_id = serializers.PrimaryKeyRelatedField(source='call', queryset=Call.objects.all())
    timestamp = serializers.DateTimeField(initial=datetime.datetime.now())
    source = serializers.CharField(min_length=10, max_length=11)
    destination = serializers.CharField(min_length=10, max_length=11)

    class Meta:
        model = CallStart
        fields = ['id', 'call_id', 'timestamp', 'source', 'destination']


class CallEndSerializer(serializers.ModelSerializer):
    call_id = serializers.PrimaryKeyRelatedField(source='call', queryset=Call.objects.all())
    timestamp = serializers.DateTimeField(initial=datetime.datetime.now())

    class Meta:
        model = CallEnd
        fields = ['id', 'call_id', 'timestamp']


class CallRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(min_length=3, max_length=5, read_only=True)
    timestamp = serializers.DateTimeField()
    source = serializers.CharField(min_length=10, max_length=11, required=False)
    destination = serializers.CharField(min_length=10, max_length=11, required=False)


class CallSerializer(serializers.ModelSerializer):
    call_id = serializers.IntegerField(source='id', required=False)
    start = CallStartSerializer(write_only=True)
    end = CallEndSerializer(write_only=True)
    records = serializers.SerializerMethodField()

    class Meta:
        model = Call
        fields = ['call_id', 'start', 'end', 'records']

    def get_records(self, obj):
        try:
            obj.start.type = 'start'
            obj.end.type = 'end'
            data = [CallRecordSerializer(obj.start).data, CallRecordSerializer(obj.end).data]
        except CallEnd.DoesNotExist:
            data = [CallRecordSerializer(obj.start).data]
        except CallStart.DoesNotExist:
            return []
        return data
