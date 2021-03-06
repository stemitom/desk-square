# Generated by Django 4.0.5 on 2022-06-23 01:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0011_alter_event_timing_type_alter_media_event_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=50,
                null=True,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Tags can only contain letters, numbers and underscores",
                        regex="^[A-Za-z0-9_]+$",
                    )
                ],
                verbose_name="tag",
            ),
        ),
    ]
