# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-26 02:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20170519_1653'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'customer'},
        ),
        migrations.AlterModelOptions(
            name='milestone',
            options={'ordering': ['deadline'], 'verbose_name': 'milestone'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'project'},
        ),
        migrations.AlterModelOptions(
            name='update',
            options={'ordering': ['-mod_date'], 'verbose_name': 'update'},
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='customer'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='deadline',
            field=models.DateField(verbose_name='deadline'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='description',
            field=models.CharField(max_length=50, verbose_name='milestone'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='is_complete',
            field=models.BooleanField(default=False, verbose_name='is complete'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projects.Project', verbose_name='project'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='remarks',
            field=models.TextField(blank=True, verbose_name='remarks'),
        ),
        migrations.AlterField(
            model_name='project',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projects.Customer', verbose_name='customer'),
        ),
        migrations.AlterField(
            model_name='project',
            name='engineer',
            field=models.ManyToManyField(to='employees.Employee', verbose_name='engineer'),
        ),
        migrations.AlterField(
            model_name='project',
            name='estimated_hours',
            field=models.SmallIntegerField(null=True, verbose_name='estimated hours'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='project name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('INP', 'In-Progress'), ('HLD', 'On Hold'), ('CND', 'Cancelled'), ('CMP', 'Completed')], max_length=3, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='project',
            name='work_type',
            field=models.CharField(choices=[('MECH', 'Mechanical'), ('ELEC', 'Electronic'), ('ASSM', 'Assembly')], max_length=4, verbose_name='project type'),
        ),
        migrations.AlterField(
            model_name='update',
            name='action_required',
            field=models.TextField(verbose_name='action required'),
        ),
        migrations.AlterField(
            model_name='update',
            name='estimated_hours',
            field=models.SmallIntegerField(verbose_name='estimated hours'),
        ),
        migrations.AlterField(
            model_name='update',
            name='mod_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='update',
            name='mod_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='update',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projects.Project', verbose_name='project'),
        ),
        migrations.AlterField(
            model_name='update',
            name='stage',
            field=models.CharField(choices=[('WCUST', 'Waiting for Customer Response'), ('MKDFM', 'Creating DFM'), ('TLDSN', 'Tooling Design'), ('TLBLD', 'Tooling Build'), ('TLTST', 'Tooling Testing'), ('TLMOD', 'Tooling Modification'), ('MKSMP', 'Creating Samples'), ('IMSMP', 'Improving Samples'), ('MK_WI', 'Creating WI'), ('MKBOM', 'Creating BOM'), ('MKECO', 'Creating ECO'), ('PRVAL', 'Process Validation'), ('PLTRN', 'Pilot Run'), ('TFBLD', 'Building Test Fixture')], max_length=5, verbose_name='stage'),
        ),
    ]
