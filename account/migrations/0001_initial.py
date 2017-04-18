# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('menu_string', models.CharField(max_length=100)),
                ('url_string', models.CharField(max_length=250)),
                ('parent_id', models.IntegerField()),
                ('group_permission_id', models.CharField(max_length=50)),
                ('isActive', models.NullBooleanField()),
                ('isDelete', models.NullBooleanField()),
                ('insertUser', models.CharField(max_length=50)),
                ('insertDate', models.DateField(null=True, blank=True)),
                ('updateUser', models.CharField(max_length=50)),
                ('updateDate', models.DateField(null=True, blank=True)),
                ('project', models.CharField(max_length=100)),
            ],
        ),
    ]
