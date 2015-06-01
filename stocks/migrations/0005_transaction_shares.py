# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_auto_20150601_0305'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='shares',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
