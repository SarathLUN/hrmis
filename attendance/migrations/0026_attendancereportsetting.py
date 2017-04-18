# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0005_employee_gender'),
        ('attendance', '0025_remove_late_sms_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceReportSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateTimeField(null=True, blank=True)),
                ('updateUser', models.CharField(null=True, max_length=50, blank=True)),
                ('updateDate', models.DateTimeField(null=True, blank=True)),
                ('project', models.CharField(null=True, max_length=100, blank=True)),
                ('child_employee', models.ForeignKey(to='hr.Employee', related_name='report_setting_child')),
                ('parent_employee', models.ForeignKey(to='hr.Employee', related_name='report_setting_parent')),
            ],
        ),
    ]
