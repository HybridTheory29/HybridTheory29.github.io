# Generated by Django 5.1.4 on 2025-01-31 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_category_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
