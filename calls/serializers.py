from rest_framework import serializers

from .models import Call, CallStart


class CallStartSerializer(serializers.ModelSerializer):
    call_id = serializers.PrimaryKeyRelatedField(source='call', queryset=Call.objects.all())

    class Meta:
        model = CallStart
        fields = ['id', 'timestamp', 'call_id', 'source', 'destination']
