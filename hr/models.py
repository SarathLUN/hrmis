from django.db import models

# Create your models here.
class Employee(models.Model):

    GENDER_IN_CHOICE = (
        ('1', 'Mr.'),
        ('2', 'Ms.')
    )

    employee_id = models.AutoField(primary_key=True)
    employeeName = models.CharField(max_length=100)
    cardId = models.CharField(max_length=20, default='0')
    joiningDate = models.DateField(blank=True, null=True)
    employeeCode = models.CharField(max_length=20)
    gender = models.CharField(max_length=6, choices=GENDER_IN_CHOICE, null=True, blank=True)
    presentAddress = models.CharField(max_length=500)
    permanentAddress = models.CharField(max_length=500)
    dateOfBirth = models.DateField(blank=True, null=True)
    fatherName = models.CharField(max_length=100)
    motherName = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=40)
    bloodGroup = models.CharField(max_length=6)
    nationality = models.CharField(max_length=25)
    nationalId = models.CharField(max_length=60)
    passportId = models.CharField(max_length=60)
    bankName = models.CharField(max_length=100)
    bankAccountNo = models.CharField(max_length=100)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)

    def __str__(self):
        return self.employeeName


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    departmentName = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, blank=True, null=True, default='')
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)

    def __str__(self):
        return self.departmentName


class DepartmentDetails(models.Model):
    deptDetail_id = models.AutoField(primary_key=True)
    departmentId = models.ForeignKey(Department)
    headOfDept = models.ForeignKey(Employee)
    startEffectiveDate = models.DateField(blank=True, null=True)
    endEffectiveDate = models.DateField(blank=True, null=True)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)



class Designation(models.Model):
    des_id = models.AutoField(primary_key=True)
    desCode = models.CharField(max_length=30)
    designation = models.CharField(max_length=70)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)

    def __str__(self):
        return self.designation


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    locationName = models.CharField(max_length=150)
    locationCode = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)

    def __str__(self):
        return self.locationName


class EmployeeDesignation(models.Model):

    STATUS_IN_CHOICE = (
        ('new', 'New'),
        ('left', 'Left'),
        ('terminated', 'Terminated'),
        ('promoted', 'Promoted'),
        ('changed', 'Changed'),
        ('transferred', 'Transferred')
    )
    emp_des_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey('Employee', related_name='employee')
    department_id = models.ForeignKey(Department)
    des_id = models.ForeignKey(Designation)
    location_id = models.ForeignKey(Location)
    effective_date_start = models.DateField(blank=True, null=True)
    effective_date_end = models.DateField(blank=True, null=True)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)
    status = models.CharField(max_length=100, null=True, blank=True)
    supervisor = models.ForeignKey('Employee', related_name='supervisor')



