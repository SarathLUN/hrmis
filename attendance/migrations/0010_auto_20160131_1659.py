# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0009_auto_20151231_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='late',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
