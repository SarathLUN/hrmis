# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_sms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='late',
            name='emp_id',
        ),
        migrations.RemoveField(
            model_name='late',
            name='endorsed_by',
        ),
        migrations.DeleteModel(
            name='Late',
        ),
    ]
