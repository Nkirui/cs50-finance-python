# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_auto_20150530_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockholding',
            name='shares',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
