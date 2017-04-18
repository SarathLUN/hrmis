# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0017_auto_20160302_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='late',
            name='insertDate',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='late',
            name='updateDate',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
