# Generated by Django 5.1 on 2024-08-09 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
