# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0014_auto_20160228_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='late',
            name='sms_text',
            field=models.CharField(max_length=500, blank=True, null=True),
        ),
    ]
