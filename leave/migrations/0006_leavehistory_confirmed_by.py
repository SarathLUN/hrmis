# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0005_employee_gender'),
        ('leave', '0005_leavecategory_confirmed_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavehistory',
            name='confirmed_by',
            field=models.ForeignKey(to='hr.Employee', null=True, blank=True, related_name='ls_confirmed_by'),
        ),
    ]
