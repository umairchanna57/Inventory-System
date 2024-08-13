# Generated by Django 5.1 on 2024-08-12 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_alter_product_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cost_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='likes',
            field=models.PositiveBigIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
