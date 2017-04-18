# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_auto_20151201_1032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='location',
        ),
        migrations.AddField(
            model_name='department',
            name='description',
            field=models.CharField(default='null', max_length=300),
        ),
    ]
