# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0022_auto_20160320_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='late',
            name='isEndorsed',
            field=models.CharField(max_length=20, choices=[('0', 'Pending'), ('1', 'Endorsed'), ('2', 'Rejected'), ('3', 'Others Endoresed'), ('4', 'Others Rejected')], default='0'),
        ),
    ]
