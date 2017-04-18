# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0024_auto_20160328_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='late',
            name='sms_type',
        ),
    ]
