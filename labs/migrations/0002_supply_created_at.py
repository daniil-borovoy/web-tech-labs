# Generated by Django 4.2.5 on 2023-11-12 12:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="supply",
            name="created_at",
            field=models.DateTimeField(
                auto_created=True, default=django.utils.timezone.now, editable=False
            ),
            preserve_default=False,
        ),
    ]
