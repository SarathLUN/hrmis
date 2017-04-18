# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0019_auto_20160308_1306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancehistory',
            old_name='field1',
            new_name='insertDtm',
        ),
    ]
