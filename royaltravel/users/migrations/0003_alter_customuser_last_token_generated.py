# Generated by Django 5.0.6 on 2024-06-15 10:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_last_token_generated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='last_token_generated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
