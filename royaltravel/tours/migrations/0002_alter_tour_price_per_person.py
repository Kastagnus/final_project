# Generated by Django 5.0.6 on 2024-06-16 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='price_per_person',
            field=models.PositiveIntegerField(help_text='Price in $'),
        ),
    ]
