# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_menutable_has_child'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menutable',
            name='parent_id',
            field=models.ForeignKey(default='-1', to='account.MenuTable'),
        ),
    ]
