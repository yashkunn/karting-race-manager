# Generated by Django 5.1.1 on 2024-09-22 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("karting", "0004_kart_available_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="race",
            name="karts_returned",
            field=models.BooleanField(default=False),
        ),
    ]
