# Generated by Django 3.1.6 on 2021-03-03 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20210303_2256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='text',
        ),
        migrations.AddField(
            model_name='productreview',
            name='text_1',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Отзыв'),
        ),
        migrations.AddField(
            model_name='productreview',
            name='text_2',
            field=models.TextField(max_length=200, null=True, verbose_name='Плюсы'),
        ),
        migrations.AddField(
            model_name='productreview',
            name='text_3',
            field=models.TextField(max_length=200, null=True, verbose_name='Минусы'),
        ),
    ]
