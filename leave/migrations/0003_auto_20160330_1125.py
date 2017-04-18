# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_leavecategory_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavecategory',
            name='gender',
            field=models.CharField(max_length=10, default='0', choices=[('0', 'All'), ('1', 'Male'), ('2', 'Female')]),
        ),
    ]
