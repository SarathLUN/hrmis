# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_regularofficetimedetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='regularofficetime',
            name='remarks',
            field=models.CharField(default='null', max_length=400),
            preserve_default=False,
        ),
    ]
