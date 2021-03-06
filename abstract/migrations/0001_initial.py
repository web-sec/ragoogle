# Generated by Django 2.0.6 on 2018-06-25 23:32

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('slug', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Ідентифікатор датасету')),
                ('name', models.TextField(verbose_name='Назва датасету')),
                ('url', models.URLField(blank=True, verbose_name='Джерело походження')),
                ('description', ckeditor.fields.RichTextField(blank=True, verbose_name='Опис набору даних')),
            ],
        ),
    ]
