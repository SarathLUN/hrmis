# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0008_regularofficetime_entry_time_with_grace'),
    ]

    operations = [
        migrations.AddField(
            model_name='regularofficetime',
            name='description',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='regularofficetime',
            name='remarks',
            field=models.CharField(max_length=24),
        ),
    ]
