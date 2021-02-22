# Generated by Django 3.1.6 on 2021-02-19 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='tag',
        ),
        migrations.AddField(
            model_name='tag',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='blog.Post'),
        ),
    ]