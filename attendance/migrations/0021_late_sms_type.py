# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0020_auto_20160313_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='late',
            name='sms_type',
            field=models.CharField(max_length=20, default='Null', null=True, blank=True),
        ),
    ]
