# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0004_auto_20160223_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='gender',
            field=models.CharField(null=True, blank=True, choices=[('1', 'Mr.'), ('2', 'Ms.')], max_length=6),
        ),
    ]
