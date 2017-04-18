# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_grouptable_menugrouptable_usergrouptable'),
    ]

    operations = [
        migrations.AddField(
            model_name='menutable',
            name='has_child',
            field=models.NullBooleanField(default='null'),
        ),
    ]
