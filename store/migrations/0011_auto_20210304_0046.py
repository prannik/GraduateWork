# Generated by Django 3.1.6 on 2021-03-03 21:46

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20210304_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='mark',
            field=models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], max_length=7),
        ),
    ]
