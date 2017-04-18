# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0005_employee_gender'),
        ('attendance', '0028_auto_20160530_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regularofficetimedetail',
            name='location_id',
        ),
        migrations.AddField(
            model_name='regularofficetime',
            name='location_id',
            field=models.ForeignKey(default='1', related_name='location_office_time_relation', to='hr.Location'),
        ),
    ]
