from django.db import models
from hr.models import Employee,Location

# Create your models here.

class AttendanceHistory(models.Model):

    ENTRY_STATUS_IN_CHOICES = (
        ('1', 'Logged in'),
        ('0', 'Logged out')
    )

    emp_card_id = models.CharField(max_length=25)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    verification = models.CharField(max_length=50)
    in_out = models.CharField(max_length=25, choices=ENTRY_STATUS_IN_CHOICES)
    workCode = models.CharField(max_length=25)
    location = models.CharField(max_length=50)
    insertDtm = models.CharField(max_length=50)
    field2 = models.CharField(max_length=50)
    field3 = models.CharField(max_length=50)


class RegularOfficeTime(models.Model):

    CATEGORY_IN_CHOICES = (
        ('1', 'Regular'),
        ('2', 'Execption')
    )

    office_start_time = models.TimeField(blank=True, null=True)
    office_end_time = models.TimeField(blank=True, null=True)
    grace_amount = models.IntegerField()
    entry_time_with_grace = models.TimeField(blank=True, null=True)
    start_effective_date = models.DateField(blank=True, null=True)
    end_effective_date = models.DateField(blank=True,null=True)
    remarks = models.CharField(max_length=24)
    description = models.CharField(max_length=400)
    entry_category = models.CharField(max_length=40, choices=CATEGORY_IN_CHOICES)
    location_id = models.ForeignKey('hr.Location', related_name='location_office_time_relation', default='1')
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)


class RegularOfficeTimeDetail(models.Model):
    date = models.DateField()
    office_start_time_with_grace = models.TimeField()
    office_end_time_with_grace = models.TimeField()
    office_start_time = models.TimeField(blank=True, null=True)
    office_end_time = models.TimeField(blank=True, null=True)
    grace_amount = models.IntegerField()
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)


class Attendance_exception(models.Model):
    date = models.DateField()
    grace_time = models.IntegerField()
    cause = models.CharField(max_length=24)
    description = models.CharField(max_length=300, blank=True, null=True)
    location_id = models.ForeignKey('hr.Location', related_name='location_office_time_exception', default='1')
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)


class sms(models.Model):
    mobile_no = models.CharField(max_length=40, blank=True,null=True)
    date_time = models.CharField(max_length=50, blank=True,null=True)
    sms_text = models.CharField(max_length=500,blank=True,null=True)
    insert_date = models.DateTimeField(blank=True,null=True)


class Late(models.Model):
    ENDORSEMENT_IN_CHOICES = (
        ('0','Pending'),
        ('1','Endorsed'),
        ('2','Rejected'),
        ('3','Others Endoresed'),
        ('4','Others Rejected'),

    )
    date = models.DateTimeField(max_length=25)
    emp_id = models.ForeignKey(Employee, related_name="attendance_employee", null=True,blank=True)
    isEndorsed = models.CharField(max_length=20,choices=ENDORSEMENT_IN_CHOICES, default='0')
    endorsed_by = models.ForeignKey(Employee, related_name="attendance_supervisor", null=True,blank=True)
    sms_text = models.CharField(max_length=500, null=True, blank=True)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateTimeField(blank=True, null=True)
    updateUser = models.CharField(max_length=50, blank=True, null=True)
    updateDate = models.DateTimeField(blank=True, null=True)
    project = models.CharField(max_length=100, blank=True, null=True)
    sms_table_id = models.ForeignKey(sms, related_name='sms_table')


class AttendanceReportSetting(models.Model):
    parent_employee = models.ForeignKey(Employee, related_name='report_setting_parent')
    child_employee = models.ForeignKey(Employee, related_name='report_setting_child')
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateTimeField(blank=True, null=True)
    updateUser = models.CharField(max_length=50, blank=True, null=True)
    updateDate = models.DateTimeField(blank=True, null=True)
    project = models.CharField(max_length=100, blank=True, null=True)

