# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0005_employee_gender'),
        ('attendance', '0027_auto_20160526_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance_exception',
            name='location_id',
            field=models.ForeignKey(related_name='location_office_time_exception', default='1', to='hr.Location'),
        ),
        migrations.AddField(
            model_name='regularofficetimedetail',
            name='location_id',
            field=models.ForeignKey(related_name='location_office_time_relation', default='1', to='hr.Location'),
        ),
    ]
