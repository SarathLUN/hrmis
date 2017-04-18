# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20160216_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeuser',
            name='updateUser',
            field=models.CharField(blank=True, null=True, default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='grouptable',
            name='updateUser',
            field=models.CharField(blank=True, null=True, default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='menugrouptable',
            name='updateUser',
            field=models.CharField(blank=True, null=True, default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='menutable',
            name='updateUser',
            field=models.CharField(blank=True, null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='usergrouptable',
            name='updateUser',
            field=models.CharField(blank=True, null=True, default=None, max_length=50),
        ),
    ]
