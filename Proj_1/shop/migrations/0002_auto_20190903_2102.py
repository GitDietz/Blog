# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-09-03 11:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='purchased',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buy_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
