from django.db import models
from hr.models import Employee, EmployeeDesignation
from datetime import date

# Create your models here.

class LeaveCategory(models.Model):

    GENDER_IN_CHOICE = (
        ('0', 'All'),
        ('1', 'Male'),
        ('2', 'Female')
    )

    APPROVE_BY_IN_CHOICE = (
        ('1', 'supervisor'),
        ('2', 'CEO'),
        ('3', 'MD')
    )

    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    effective_day_from = models.DateField(blank=True, null=True)
    effective_day_to = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=300, default=None)
    gender = models.CharField(max_length=10, default='0', choices=GENDER_IN_CHOICE)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)
    confirmed_by = models.ForeignKey(Employee, null=True, blank=True)
    leave_type = models.IntegerField(default=0)
    entitled = models.IntegerField(default=0) #new leave edit
    validity = models.IntegerField(default=0)
    minimumdays = models.IntegerField(default=0)
    holiday_skip = models.NullBooleanField()
    is_forward = models.NullBooleanField()
    forward_validity = models.IntegerField(default=0)
    pre_condition = models.IntegerField(default=0)

class EmployeeLeaveSetting(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_category = models.ForeignKey(LeaveCategory, on_delete=models.CASCADE)
    frequency = models.IntegerField()
    year = models.IntegerField(default=date.today().year)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)


class LeaveHistory(models.Model):

    ENDORSEMENT_IN_CHOICES = (
        ('0','Pending'),
        ('1','Endorsed'),
        ('2','Rejected'),
        ('3','Recommanded'),

    )
    employee_id = models.ForeignKey('hr.Employee', related_name='ls_employee')
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    count = models.IntegerField()
    type = models.ForeignKey(LeaveCategory)
    endorsement = models.CharField(max_length=20,choices=ENDORSEMENT_IN_CHOICES)
    endorsed_by = models.ForeignKey('hr.Employee', related_name='ls_supervisor')
    confirmed_by = models.ForeignKey('hr.Employee', related_name='ls_confirmed_by', null=True, blank=True)
    description = models.CharField(max_length=300)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)


class LeaveAllotment(models.Model):
    employee_id = models.ForeignKey('hr.Employee', related_name='la_employee')
    year = models.CharField(max_length=20)
    leave_id = models.OneToOneField(LeaveHistory, related_name="leave_history_table", on_delete=models.CASCADE)
    balance = models.IntegerField()
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)
    insertType = models.CharField(max_length=30, default='0')
    frequency_count = models.IntegerField(null=True, blank=True, default=0)


class LeaveDetail(models.Model):
    date = models.DateField()
    leave_id = models.ForeignKey(LeaveHistory, on_delete=models.CASCADE)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)

'''
class AbsentHistory(models.Model):
    IN_OUT_STATUS_IN_CHOICE = (
        ('1', 'IN'),
        ('0', 'OUT')
    )
    reason_type = models.CharField(max_length=100)
    in_out = models.CharField(max_length=20, choices=IN_OUT_STATUS_IN_CHOICE, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    applied_by = models.ForeignKey(Employee)

    '''

