# Generated by Django 2.0.10 on 2020-04-28 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.IntegerField(max_length=100, verbose_name='分数'),
        ),
    ]
