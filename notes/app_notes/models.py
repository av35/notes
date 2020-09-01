from django.db import models


class Note(models.Model):
    event = models.CharField(max_length=4096)
    when = models.DateTimeField()
