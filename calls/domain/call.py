from django.db import models

from calls.exceptions import CallStartMissingError, TimestampLessThanCallStartTimestampError
from calls.exceptions import TimestampGreaterThanCallEndTimestampError


class Call(models.Model):
    def __str__(self):
        return 'call_id: {}'.format(self.id)

    def get_duration(self, in_minutes=False):
        duration = self.end.timestamp - self.start.timestamp
        if in_minutes:
            minutes, seconds = divmod(duration.total_seconds(), 60)
            return minutes
        else:
            return duration


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

        return super().save(*args, **kwargs)


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

        return super().save(*args, **kwargs)
