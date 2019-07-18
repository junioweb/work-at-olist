from django.db import models

from .exceptions import CallStartMissingError, TimestampLessThanCallStartTimestampError
from .exceptions import TimestampGreaterThanCallEndTimestampError


class Call(models.Model):

    def __str__(self):
        return 'call_id: {}'.format(self.id)


class CallStart(models.Model):
    call = models.OneToOneField(Call, related_name='start', on_delete=models.CASCADE)
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ['call_id']

    def __str__(self):
        return 'call_id: {}, started at {}'.format(self.call.id, self.timestamp)

    def save(self, *args, **kwargs):
        if self.id:
            try:
                if self.timestamp > self.call.end.timestamp:
                    raise TimestampGreaterThanCallEndTimestampError()
            except CallEnd.DoesNotExist:
                return super().save(*args, **kwargs)

        super().save(*args, **kwargs)


class CallEnd(models.Model):
    call = models.OneToOneField(Call, related_name='end', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ['call_id']

    def __str__(self):
        return 'call_id: {}, ended at {}'.format(self.call.id, self.timestamp)

    def save(self, *args, **kwargs):
        if not CallStart.objects.filter(call=self.call).exists():
            raise CallStartMissingError()
        if self.timestamp < self.call.start.timestamp:
            raise TimestampLessThanCallStartTimestampError()

        super().save(*args, **kwargs)
