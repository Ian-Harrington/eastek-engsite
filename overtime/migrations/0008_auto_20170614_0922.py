# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-14 01:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('overtime', '0007_auto_20170526_1001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='overtime',
            options={'ordering': ['-date'], 'permissions': (('view_overtime', 'Can view overtime'),), 'verbose_name': 'overtime', 'verbose_name_plural': 'overtime'},
        ),
    ]
