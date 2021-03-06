# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-01 00:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20170526_1001'),
        ('users', '0004_remove_user_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='link1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='link2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='link3',
        ),
        migrations.AddField(
            model_name='user',
            name='projlink1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user1', to='projects.Project', verbose_name='link 1'),
        ),
        migrations.AddField(
            model_name='user',
            name='projlink2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user2', to='projects.Project', verbose_name='link 2'),
        ),
        migrations.AddField(
            model_name='user',
            name='projlink3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user3', to='projects.Project', verbose_name='link 3'),
        ),
        migrations.AlterField(
            model_name='user',
            name='link1txt',
            field=models.CharField(blank=True, max_length=17, verbose_name='link 1 text'),
        ),
        migrations.AlterField(
            model_name='user',
            name='link2txt',
            field=models.CharField(blank=True, max_length=17, verbose_name='link 2 text'),
        ),
        migrations.AlterField(
            model_name='user',
            name='link3txt',
            field=models.CharField(blank=True, max_length=17, verbose_name='link 3 text'),
        ),
    ]
