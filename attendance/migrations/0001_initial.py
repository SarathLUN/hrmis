# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceHistory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('emp_card_id', models.CharField(max_length=25)),
                ('date', models.DateField(null=True, blank=True)),
                ('time', models.TimeField(null=True, blank=True)),
                ('verification', models.CharField(max_length=50)),
                ('in_out', models.CharField(max_length=25)),
                ('workCode', models.CharField(max_length=25)),
                ('location', models.CharField(max_length=50)),
                ('field1', models.CharField(max_length=50)),
                ('field2', models.CharField(max_length=50)),
                ('field3', models.CharField(max_length=50)),
            ],
        ),
    ]
