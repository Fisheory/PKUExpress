# Generated by Django 5.1.2 on 2024-12-11 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_customuser_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="user_images"),
        ),
    ]