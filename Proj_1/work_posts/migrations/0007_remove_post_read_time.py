# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-08-15 10:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work_posts', '0006_post_read_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='read_time',
        ),
    ]