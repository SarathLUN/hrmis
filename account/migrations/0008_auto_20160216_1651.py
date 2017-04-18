# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20160207_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeuser',
            name='insertDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='employeeuser',
            name='insertUser',
            field=models.CharField(max_length=50, default='system'),
        ),
        migrations.AddField(
            model_name='employeeuser',
            name='isActive',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeeuser',
            name='isDelete',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeeuser',
            name='project',
            field=models.CharField(max_length=100, default='1'),
        ),
        migrations.AddField(
            model_name='employeeuser',
            name='updateDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='employeeuser',
            name='updateUser',
            field=models.CharField(max_length=50, default=None),
        ),
        migrations.AddField(
            model_name='grouptable',
            name='insertDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='grouptable',
            name='insertUser',
            field=models.CharField(max_length=50, default='system'),
        ),
        migrations.AddField(
            model_name='grouptable',
            name='isActive',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AddField(
            model_name='grouptable',
            name='isDelete',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='grouptable',
            name='project',
            field=models.CharField(max_length=100, default='1'),
        ),
        migrations.AddField(
            model_name='grouptable',
            name='updateDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='grouptable',
            name='updateUser',
            field=models.CharField(max_length=50, default=None),
        ),
        migrations.AddField(
            model_name='menugrouptable',
            name='insertDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='menugrouptable',
            name='insertUser',
            field=models.CharField(max_length=50, default='system'),
        ),
        migrations.AddField(
            model_name='menugrouptable',
            name='isActive',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AddField(
            model_name='menugrouptable',
            name='isDelete',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='menugrouptable',
            name='project',
            field=models.CharField(max_length=100, default='1'),
        ),
        migrations.AddField(
            model_name='menugrouptable',
            name='updateDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='menugrouptable',
            name='updateUser',
            field=models.CharField(max_length=50, default=None),
        ),
        migrations.AddField(
            model_name='usergrouptable',
            name='insertDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='usergrouptable',
            name='insertUser',
            field=models.CharField(max_length=50, default='system'),
        ),
        migrations.AddField(
            model_name='usergrouptable',
            name='isActive',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usergrouptable',
            name='isDelete',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usergrouptable',
            name='project',
            field=models.CharField(max_length=100, default='1'),
        ),
        migrations.AddField(
            model_name='usergrouptable',
            name='updateDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='usergrouptable',
            name='updateUser',
            field=models.CharField(max_length=50, default=None),
        ),
    ]
