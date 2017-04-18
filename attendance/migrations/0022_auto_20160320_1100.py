# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0021_late_sms_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='late',
            name='isEndorsed',
            field=models.CharField(default='0', choices=[('0', 'Pending'), ('1', 'Endorsed'), ('2', 'Rejected'), ('3', 'Others Endoresed'), ('4', 'Others Reject')], max_length=20),
        ),
    ]
