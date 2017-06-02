# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-26 02:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import overtime.models


class Migration(migrations.Migration):

    dependencies = [
        ('overtime', '0006_auto_20170510_0907'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='overtime',
            options={'ordering': ['-date'], 'permissions': (('view_overtime', 'Can view overtime submissions'),), 'verbose_name': 'overtime', 'verbose_name_plural': 'overtime'},
        ),
        migrations.AlterField(
            model_name='overtime',
            name='actual_hours',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[overtime.models.Overtime.validate_hours], verbose_name='hours worked'),
        ),
        migrations.AlterField(
            model_name='overtime',
            name='date',
            field=models.DateField(verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='overtime',
            name='emp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='overtime', to='employees.Employee', verbose_name='employee'),
        ),
        migrations.AlterField(
            model_name='overtime',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projects.Project', verbose_name='project'),
        ),
        migrations.AlterField(
            model_name='overtime',
            name='reason',
            field=models.CharField(max_length=120, verbose_name='reason'),
        ),
        migrations.AlterField(
            model_name='overtime',
            name='request_hours',
            field=models.DecimalField(decimal_places=1, max_digits=3, validators=[overtime.models.Overtime.validate_hours], verbose_name='request hours'),
        ),
        migrations.AlterField(
            model_name='overtime',
            name='time',
            field=models.TimeField(verbose_name='time'),
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
