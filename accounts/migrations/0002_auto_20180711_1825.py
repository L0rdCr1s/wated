# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-11 18:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('sautiYangu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituteprofile',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sautiYangu.Category'),
        ),
        migrations.AddField(
            model_name='instituteprofile',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['user_role'], name='accounts_cu_user_ro_df09fd_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['email'], name='accounts_cu_email_5ce40b_idx'),
        ),
        migrations.AddIndex(
            model_name='userprofile',
            index=models.Index(fields=['user'], name='accounts_us_user_id_806298_idx'),
        ),
        migrations.AddIndex(
            model_name='userprofile',
            index=models.Index(fields=['date_of_birth'], name='accounts_us_date_of_20d27a_idx'),
        ),
        migrations.AddIndex(
            model_name='instituteprofile',
            index=models.Index(fields=['institute'], name='accounts_in_institu_f3ed9e_idx'),
        ),
    ]
