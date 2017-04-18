# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0004_auto_20160223_1045'),
        ('attendance', '0012_auto_20160225_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='Late',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField()),
                ('isEndorsed', models.NullBooleanField()),
                ('sms_text', models.CharField(max_length=500)),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(blank=True, null=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(blank=True, null=True)),
                ('project', models.CharField(max_length=100)),
                ('emp_id', models.ForeignKey(related_name='attendance_employee', to='hr.Employee')),
                ('endorsed_by', models.ForeignKey(related_name='attendance_supervisor', to='hr.Employee')),
                ('sms_table_id', models.ForeignKey(related_name='sms_table', to='attendance.sms')),
            ],
        ),
    ]
