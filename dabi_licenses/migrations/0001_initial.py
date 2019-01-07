# Generated by Django 2.0.7 on 2019-01-06 23:32

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DabiLicenseModel',
            fields=[
                ('id', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Хеш')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(null=True, verbose_name='Дані')),
                ('last_updated_from_dataset', models.DateTimeField(null=True, verbose_name='Останній раз завантажено')),
                ('first_updated_from_dataset', models.DateTimeField(null=True, verbose_name='Перший раз завантажено')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]