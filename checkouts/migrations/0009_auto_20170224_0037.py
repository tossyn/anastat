# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-23 23:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkouts', '0008_auto_20170222_1725'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checkout',
            options={'permissions': (('can_approve_transaction', 'Approve transaction approval request sent to affiliate manager'), ('can_disapprove_transaction', 'Disapprove transaction apprroval request  sent to affiliate manager'))},
        ),
        migrations.AddField(
            model_name='checkout',
            name='approved_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]