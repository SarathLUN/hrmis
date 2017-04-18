# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0003_auto_20160330_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveallotment',
            name='insertType',
            field=models.CharField(max_length=30, default='0'),
        ),
    ]
