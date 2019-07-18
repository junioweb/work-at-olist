from rest_framework import serializers

from .models import Call, CallEnd, CallStart


class CallStartSerializer(serializers.ModelSerializer):
    call_id = serializers.PrimaryKeyRelatedField(source='call', queryset=Call.objects.all())
    type = serializers.CharField(default='start', max_length=5, read_only=True)

    class Meta:
        model = CallStart
        fields = ['id', 'type', 'timestamp', 'call_id', 'source', 'destination']


class CallEndSerializer(serializers.ModelSerializer):
    call_id = serializers.PrimaryKeyRelatedField(source='call', queryset=Call.objects.all())
    type = serializers.CharField(default='end', max_length=3, read_only=True)

    class Meta:
        model = CallEnd
        fields = ['id', 'type', 'timestamp', 'call_id']


class CallSerializer(serializers.ModelSerializer):
    start = CallStartSerializer()
    end = CallEndSerializer(required=False)

    class Meta:
        model = Call
        fields = ['start', 'end']
