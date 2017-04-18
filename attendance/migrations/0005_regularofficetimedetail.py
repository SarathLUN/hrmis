# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_late'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegularOfficeTimeDetail',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateField()),
                ('office_start_time_with_grace', models.TimeField()),
                ('office_end_time_with_grace', models.TimeField()),
                ('office_start_time', models.TimeField(null=True, blank=True)),
                ('office_end_time', models.TimeField(null=True, blank=True)),
                ('grace_amount', models.IntegerField()),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(null=True, blank=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(null=True, blank=True)),
                ('project', models.CharField(max_length=100)),
            ],
        ),
    ]
