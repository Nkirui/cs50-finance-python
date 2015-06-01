# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_auto_20150526_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockholding',
            name='shares',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='price',
        ),
        migrations.AlterField(
            model_name='financeuser',
            name='cash',
            field=models.FloatField(default=10000),
        ),
        migrations.AlterField(
            model_name='stockholding',
            name='owner',
            field=models.ForeignKey(to='stocks.FinanceUser'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.IntegerField(choices=[(1, 'buy'), (2, 'sell')]),
        ),
    ]
