# Generated by Django 5.1.4 on 2025-01-28 19:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_task_created_category_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
