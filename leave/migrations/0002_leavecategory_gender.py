# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavecategory',
            name='gender',
            field=models.CharField(choices=[('0', 'All'), ('1', 'Mr.'), ('2', 'Ms.')], max_length=10, default='0'),
        ),
    ]
