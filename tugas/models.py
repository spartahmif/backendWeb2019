from django.db import models
import datetime

# Create your models here.
class Tugas(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    