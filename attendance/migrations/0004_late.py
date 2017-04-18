# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_auto_20151201_1032'),
        ('attendance', '0003_attendance_exception_regularofficetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Late',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateField()),
                ('isEndorsed', models.NullBooleanField()),
                ('sms_text', models.CharField(max_length=500)),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(null=True, blank=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(null=True, blank=True)),
                ('project', models.CharField(max_length=100)),
                ('emp_id', models.ForeignKey(to='hr.Employee', related_name='attendance_employee')),
                ('endorsed_by', models.ForeignKey(to='hr.Employee', related_name='attendance_supervisor')),
            ],
        ),
    ]
