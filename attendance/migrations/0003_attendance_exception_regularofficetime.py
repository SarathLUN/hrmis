# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_auto_20151207_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance_exception',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date', models.DateField()),
                ('grace_time', models.IntegerField()),
                ('cause', models.CharField(max_length=350)),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(blank=True, null=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(blank=True, null=True)),
                ('project', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RegularOfficeTime',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('office_start_time', models.TimeField(blank=True, null=True)),
                ('office_end_time', models.TimeField(blank=True, null=True)),
                ('grace_amount', models.IntegerField()),
                ('start_effective_date', models.DateField(blank=True, null=True)),
                ('end_effective_date', models.DateField(blank=True, null=True)),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(blank=True, null=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(blank=True, null=True)),
                ('project', models.CharField(max_length=100)),
            ],
        ),
    ]
