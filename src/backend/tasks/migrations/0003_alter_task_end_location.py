# Generated by Django 5.1.2 on 2024-11-12 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_end_location_task_start_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='end_location',
            field=models.CharField(max_length=100),
        ),
    ]
