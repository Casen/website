# Generated by Django 2.0.3 on 2018-03-10 00:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect_four', '0002_auto_20180310_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='player',
            field=models.IntegerField(default=None, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(1)]),
        ),
    ]
