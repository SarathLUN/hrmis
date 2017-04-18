from django.db import models
from hr.models import Location

# Create your models here.
class WeeklyHoliday(models.Model):
    dayNum = models.IntegerField()
    dayName = models.CharField(max_length=15)
    effectiveFrom = models.DateField(blank=True, null=True)
    effectiveEnd = models.DateField(blank=True, null=True)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)
    active_location = models.ForeignKey(Location, default=None, null=True, blank=True)


class WeekDays(models.Model):
    dayname = models.CharField(max_length=20)
    dayNum = models.IntegerField()
    status = models.BooleanField()


class YearlyHoliday(models.Model):
    holidayTitle = models.CharField(max_length=250)
    date = models.DateField(blank=True, null=True)
    year = models.CharField(max_length=6)
    description = models.CharField(max_length=500)
    flag = models.IntegerField(null=True)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)