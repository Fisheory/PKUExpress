# Generated by Django 4.2.16 on 2024-11-09 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('to_be_accepted', 'to_be_accepted'), ('accepted', 'accepted'), ('finished', 'finished'), ('out_of_date', 'out_of_date')], default='to_be_accepted', max_length=20),
        ),
    ]
