# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0015_auto_20160228_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='late',
            name='isEndorsed',
            field=models.NullBooleanField(choices=[(True, 'Endorsed'), (False, 'Unendorsed')]),
        ),
    ]
