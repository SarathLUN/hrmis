# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_employeeuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menutable',
            name='parent_id',
            field=models.ForeignKey(to='account.MenuTable', null=True),
        ),
    ]
