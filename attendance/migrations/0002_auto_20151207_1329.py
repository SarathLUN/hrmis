# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancehistory',
            name='in_out',
            field=models.CharField(max_length=25, choices=[('1', 'Logged in'), ('0', 'Logged out')]),
        ),
    ]
