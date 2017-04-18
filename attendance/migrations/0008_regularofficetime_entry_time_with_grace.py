# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_regularofficetime_entry_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='regularofficetime',
            name='entry_time_with_grace',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
