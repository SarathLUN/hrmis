# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20160203_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menutable',
            name='parent_id',
            field=models.ForeignKey(null=True, blank=True, to='account.MenuTable'),
        ),
    ]
