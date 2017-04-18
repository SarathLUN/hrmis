# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0023_auto_20160320_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance_exception',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='attendance_exception',
            name='cause',
            field=models.CharField(max_length=24),
        ),
    ]
