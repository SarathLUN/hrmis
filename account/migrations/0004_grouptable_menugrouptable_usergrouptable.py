# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20160201_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupTable',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('group_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MenuGroupTable',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('menu_group_id', models.ForeignKey(to='account.GroupTable')),
                ('menu_id', models.ForeignKey(to='account.MenuTable')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroupTable',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('group_id', models.ForeignKey(to='account.GroupTable')),
                ('user_id', models.ForeignKey(to='account.EmployeeUser')),
            ],
        ),
    ]
