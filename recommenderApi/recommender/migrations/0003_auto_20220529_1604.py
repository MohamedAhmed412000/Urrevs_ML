# Generated by Django 3.2.13 on 2022-05-29 14:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0002_creview_preview_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='CQ',
            field=models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(6)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='CR',
            field=models.IntegerField(default=4, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='PQ',
            field=models.IntegerField(default=6, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(6)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='PR',
            field=models.IntegerField(default=8, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(14)]),
        ),
    ]
