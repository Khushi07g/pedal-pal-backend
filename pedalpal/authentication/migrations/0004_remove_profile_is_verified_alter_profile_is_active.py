# Generated by Django 4.2.10 on 2024-03-15 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_profile_is_verified_profile_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_verified',
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]