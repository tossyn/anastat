# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-04 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0010_auto_20170204_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrequest',
            name='categories_of_aggregation',
        ),
        migrations.AddField(
            model_name='userrequest',
            name='categories_of_aggregation',
            field=models.ManyToManyField(to='sales.CategoryOfAggregation'),
        ),
    ]
