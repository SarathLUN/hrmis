# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('departmentName', models.CharField(max_length=100, unique=True)),
                ('location', models.CharField(max_length=100, default='null')),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(null=True, blank=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(null=True, blank=True)),
                ('project', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentDetails',
            fields=[
                ('deptDetail_id', models.AutoField(primary_key=True, serialize=False)),
                ('startEffectiveDate', models.DateField(null=True, blank=True)),
                ('endEffectiveDate', models.DateField(null=True, blank=True)),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(null=True, blank=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(null=True, blank=True)),
                ('project', models.CharField(max_length=100)),
                ('departmentId', models.ForeignKey(to='hr.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('des_id', models.AutoField(primary_key=True, serialize=False)),
                ('desCode', models.CharField(max_length=30)),
                ('designation', models.CharField(max_length=70)),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(null=True, blank=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(null=True, blank=True)),
                ('project', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('employeeCode', models.CharField(max_length=20)),
                ('cardId', models.CharField(max_length=20, default='0')),
                ('joiningDate', models.DateField(null=True, blank=True)),
                ('employeeName', models.CharField(max_length=100)),
                ('presentAddress', models.CharField(max_length=500)),
                ('permanentAddress', models.CharField(max_length=500)),
                ('dateOfBirth', models.DateField(null=True, blank=True)),
                ('fatherName', models.CharField(max_length=100)),
                ('motherName', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=15)),
                ('bloodGroup', models.CharField(max_length=6)),
                ('nationality', models.CharField(max_length=25)),
                ('nationalId', models.CharField(max_length=60)),
                ('passportId', models.CharField(max_length=60)),
                ('bankName', models.CharField(max_length=100)),
                ('bankAccountNo', models.CharField(max_length=100)),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(null=True, blank=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(null=True, blank=True)),
                ('project', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeDesignation',
            fields=[
                ('emp_des_id', models.AutoField(primary_key=True, serialize=False)),
                ('effective_date_start', models.DateField(null=True, blank=True)),
                ('effective_date_end', models.DateField(null=True, blank=True)),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(null=True, blank=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(null=True, blank=True)),
                ('project', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('department_id', models.ForeignKey(to='hr.Department')),
                ('des_id', models.ForeignKey(to='hr.Designation')),
                ('employee_id', models.ForeignKey(to='hr.Employee', related_name='employee')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('locationName', models.CharField(max_length=150)),
                ('locationCode', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=250)),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(null=True, blank=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(null=True, blank=True)),
                ('project', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='employeedesignation',
            name='location_id',
            field=models.ForeignKey(to='hr.Location'),
        ),
        migrations.AddField(
            model_name='employeedesignation',
            name='supervisor',
            field=models.ForeignKey(to='hr.Employee', related_name='supervisor'),
        ),
        migrations.AddField(
            model_name='departmentdetails',
            name='headOfDept',
            field=models.ForeignKey(to='hr.Employee'),
        ),
    ]
