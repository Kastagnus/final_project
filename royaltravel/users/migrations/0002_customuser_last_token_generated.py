# Generated by Django 5.0.6 on 2024-06-15 10:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='last_token_generated',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 15, 10, 5, 32, 974477, tzinfo=datetime.timezone.utc)),
        ),
    ]
