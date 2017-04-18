# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_regularofficetime_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='regularofficetime',
            name='entry_category',
            field=models.CharField(max_length=40, default=1, choices=[('1', 'Regular'), ('2', 'Execption')]),
            preserve_default=False,
        ),
    ]
