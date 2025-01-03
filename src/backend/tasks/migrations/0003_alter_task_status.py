# Generated by Django 5.1.2 on 2024-12-25 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('to_be_accepted', 'to_be_accepted'), ('accepted', 'accepted'), ('finished', 'finished'), ('ack_finished', 'ack_finished'), ('out_of_date', 'out_of_date')], default='to_be_accepted', max_length=20),
        ),
    ]
