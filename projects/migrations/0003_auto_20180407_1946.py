# Generated by Django 2.0.3 on 2018-04-07 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20180330_2355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='custom_template',
        ),
        migrations.AddField(
            model_name='project',
            name='content',
            field=models.TextField(default=''),
        ),
    ]