# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-21 19:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.CharField(max_length=50, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.CharField(max_length=50, unique=True)),
                ('image_url', models.CharField(max_length=500, null=True)),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(null=True)),
                ('added_date', models.DateTimeField()),
                ('is_public', models.BooleanField(default=False)),
                ('is_family', models.BooleanField(default=False)),
                ('is_friend', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='photos.Group')),
            ],
        ),
    ]
