from rest_framework import serializers

from .models import CallStart


class CallStartSerializer(serializers.ModelSerializer):
    call_id = serializers.ReadOnlyField(source='call.id')

    class Meta:
        model = CallStart
        fields = ['id', 'timestamp', 'call_id', 'source', 'destination']
