# Generated by Django 5.1.2 on 2024-12-11 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myMessages", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="text",
            field=models.TextField(blank=True, null=True),
        ),
    ]
