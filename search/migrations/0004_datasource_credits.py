# Generated by Django 2.2.4 on 2019-09-08 12:01

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_datasource'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasource',
            name='credits',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Хто надав набір даних'),
        ),
    ]
