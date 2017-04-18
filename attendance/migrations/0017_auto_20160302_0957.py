# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0016_auto_20160229_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='late',
            name='date',
            field=models.DateTimeField(max_length=6),
        ),
    ]
