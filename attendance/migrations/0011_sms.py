# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0010_auto_20160131_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='sms',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('mobile_no', models.CharField(max_length=40, blank=True, null=True)),
                ('date_time', models.CharField(max_length=50, blank=True, null=True)),
                ('sms_text', models.CharField(max_length=500, blank=True, null=True)),
                ('insert_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
