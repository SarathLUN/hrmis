# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0005_employee_gender'),
        ('leave', '0004_leaveallotment_inserttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavecategory',
            name='confirmed_by',
            field=models.ForeignKey(null=True, blank=True, to='hr.Employee'),
        ),
    ]
