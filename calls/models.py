from django.db import models


class Call(models.Model):

    def __str__(self):
        return 'call_id: {}, started at {} and ended at {}'.format(self.id, self.start.timestamp, self.end.timestamp)


class CallStart(models.Model):
    call = models.OneToOneField(Call, related_name='start', on_delete=models.CASCADE)
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)
    timestamp = models.DateTimeField()

    def __str__(self):
        return 'call_id: {}, started at {}'.format(self.call.id, self.timestamp)


class CallEnd(models.Model):
    call = models.OneToOneField(Call, related_name='end', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return 'call_id: {}, ended at {}'.format(self.call.id, self.timestamp)
