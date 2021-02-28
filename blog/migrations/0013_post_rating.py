# Generated by Django 3.1.6 on 2021-02-26 22:32

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=Decimal('3.00'), max_digits=3),
        ),
    ]
