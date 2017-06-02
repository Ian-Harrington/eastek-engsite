# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-01 00:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_auto_20170531_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='team',
            field=models.CharField(choices=[('MECH', 'Mechanical'), ('ELEC', 'Electronics'), ('SUPP', 'Support'), ('TOOL', 'Tooling')], max_length=4, verbose_name='team'),
        ),
    ]
