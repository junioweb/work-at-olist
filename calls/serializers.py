from rest_framework import serializers

from .models import Call, CallEnd, CallStart


class CallStartSerializer(serializers.ModelSerializer):
    call_id = serializers.PrimaryKeyRelatedField(source='call', queryset=Call.objects.all())

    class Meta:
        model = CallStart
        fields = ['id', 'timestamp', 'call_id', 'source', 'destination']


class CallEndSerializer(serializers.ModelSerializer):
    call_id = serializers.PrimaryKeyRelatedField(source='call', queryset=Call.objects.all())

    class Meta:
        model = CallEnd
        fields = ['id', 'timestamp', 'call_id']
