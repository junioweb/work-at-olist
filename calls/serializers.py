import datetime

from rest_framework import serializers

from calls.domain.call import Call, CallEnd, CallStart

from .exceptions import TypeCallMissingError


class CallRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(min_length=3, max_length=5)
    timestamp = serializers.DateTimeField(initial=datetime.datetime.now())
    source = serializers.CharField(min_length=10, max_length=11, required=False)
    destination = serializers.CharField(min_length=10, max_length=11, required=False)

    def update(self, instance, validated_data):
        type_call = validated_data.pop('type', None)

        if not self.partial and type_call is None:
            raise TypeCallMissingError()

        instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        if type_call == 'start':
            instance.source = validated_data.get('source', instance.source)
            instance.destination = validated_data.get('destination', instance.destination)
        instance.save()
        return instance

    def create(self, validated_data):
        type_call = validated_data.pop('type', None)

        if type_call is None:
            raise TypeCallMissingError()

        if type_call == 'start':
            return CallStart.objects.create(**validated_data)
        elif type_call == 'end':
            return CallEnd.objects.create(**validated_data)


class CallStartSerializer(CallRecordSerializer):
    call_id = serializers.PrimaryKeyRelatedField(source='call', queryset=Call.objects.all())
    type = serializers.CharField(initial='start', max_length=5, write_only=True)


class CallEndSerializer(CallRecordSerializer):
    call_id = serializers.PrimaryKeyRelatedField(source='call', queryset=Call.objects.all())
    type = serializers.CharField(initial='end', max_length=3, write_only=True)
    source = None
    destination = None


class CallSerializer(serializers.ModelSerializer):
    call_id = serializers.IntegerField(source='id', required=False)
    records = serializers.SerializerMethodField()

    class Meta:
        model = Call
        fields = ['call_id', 'records']

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
