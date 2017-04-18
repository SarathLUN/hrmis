# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0003_auto_20160223_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='description',
            field=models.CharField(max_length=300, blank=True, null=True, default=''),
        ),
    ]
