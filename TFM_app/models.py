from django.db import models

# Create your models here.
class PredResults(models.Model):

    sensor_02 = models.IntegerField()
    sensor_04 = models.IntegerField()
    sensor_06 = models.IntegerField()
    sensor_10 = models.IntegerField()
    sensor_11 = models.IntegerField()
    sensor_12 = models.IntegerField()
    machine_status = models.CharField(max_length=30)
    

    def __str__(self):
        return self.machine_status