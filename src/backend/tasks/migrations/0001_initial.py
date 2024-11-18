# Generated by Django 5.1.2 on 2024-11-18 15:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('reward', models.IntegerField()),
                ('start_location', models.CharField(blank=True, max_length=100, null=True)),
                ('end_location', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('finish_time', models.DateTimeField(blank=True, null=True)),
                ('deadline', models.DateTimeField()),
                ('status', models.CharField(choices=[('to_be_accepted', 'to_be_accepted'), ('accepted', 'accepted'), ('finished', 'finished'), ('out_of_date', 'out_of_date')], default='to_be_accepted', max_length=20)),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='published_tasks', to=settings.AUTH_USER_MODEL)),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepted_tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]