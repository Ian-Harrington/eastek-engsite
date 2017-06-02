# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-20 07:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_employee_leader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='leader',
            field=models.ForeignKey(default='00001', on_delete=django.db.models.deletion.PROTECT, to='employees.Employee'),
            preserve_default=False,
        ),
    ]
