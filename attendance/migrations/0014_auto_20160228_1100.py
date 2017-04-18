# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0013_late'),
    ]

    operations = [
        migrations.AlterField(
            model_name='late',
            name='emp_id',
            field=models.ForeignKey(to='hr.Employee', null=True, related_name='attendance_employee', blank=True),
        ),
        migrations.AlterField(
            model_name='late',
            name='endorsed_by',
            field=models.ForeignKey(to='hr.Employee', null=True, related_name='attendance_supervisor', blank=True),
        ),
        migrations.AlterField(
            model_name='late',
            name='project',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='late',
            name='updateUser',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
