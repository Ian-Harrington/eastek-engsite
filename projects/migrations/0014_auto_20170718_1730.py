# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 09:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_auto_20170717_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='lead_eng',
        ),
        migrations.AlterField(
            model_name='checklistitem',
            name='name',
            field=models.CharField(max_length=140, verbose_name='item'),
        ),
        migrations.AlterField(
            model_name='checklistitem',
            name='remarks',
            field=models.CharField(blank=True, max_length=140, verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=80, unique=True, verbose_name='customer'),
        ),
        migrations.AlterField(
            model_name='project',
            name='cust_pn',
            field=models.CharField(blank=True, max_length=85, verbose_name='customer part number'),
        ),
        migrations.AlterField(
            model_name='project',
            name='eastek_pn',
            field=models.CharField(blank=True, max_length=85, verbose_name='eastek part number'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=120, verbose_name='project name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='work_type',
            field=models.CharField(choices=[('M', 'Mechanical'), ('E', 'Electronic'), ('A', 'Assembly'), ('ME', 'Mechanical/Electronic'), ('MA', 'Mechanical/Assembly'), ('EA', 'Electronic/Assembly'), ('MEA', 'Mechanical/Electronic/Assembly')], max_length=3, verbose_name='project type'),
        ),
    ]