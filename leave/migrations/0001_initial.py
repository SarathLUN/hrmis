# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0004_auto_20160223_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveAllotment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('year', models.CharField(max_length=20)),
                ('balance', models.IntegerField()),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(null=True, blank=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(null=True, blank=True)),
                ('project', models.CharField(max_length=100)),
                ('employee_id', models.ForeignKey(related_name='la_employee', to='hr.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveCategory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('effective_day_from', models.DateField(null=True, blank=True)),
                ('effective_day_to', models.DateField(null=True, blank=True)),
                ('description', models.CharField(max_length=300, default=None)),
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
            name='LeaveDetail',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('date', models.DateField()),
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
            name='LeaveHistory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('date_from', models.DateField(null=True, blank=True)),
                ('date_to', models.DateField(null=True, blank=True)),
                ('count', models.IntegerField()),
                ('endorsement', models.CharField(choices=[('0', 'Pending'), ('1', 'Endorsed'), ('2', 'Rejected')], max_length=20)),
                ('description', models.CharField(max_length=300)),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(null=True, blank=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(null=True, blank=True)),
                ('project', models.CharField(max_length=100)),
                ('employee_id', models.ForeignKey(related_name='ls_employee', to='hr.Employee')),
                ('endorsed_by', models.ForeignKey(related_name='ls_supervisor', to='hr.Employee')),
                ('type', models.ForeignKey(to='leave.LeaveCategory')),
            ],
        ),
        migrations.AddField(
            model_name='leavedetail',
            name='leave_id',
            field=models.ForeignKey(to='leave.LeaveHistory'),
        ),
        migrations.AddField(
            model_name='leaveallotment',
            name='leave_id',
            field=models.ForeignKey(to='leave.LeaveHistory'),
        ),
    ]
