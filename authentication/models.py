from django.db import models

class YourModel(models.Model):
    category = models.CharField(max_length=100)
    value = models.IntegerField()

    class Meta:
        app_label = 'authentication'

