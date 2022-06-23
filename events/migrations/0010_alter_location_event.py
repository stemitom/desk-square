# Generated by Django 4.0.5 on 2022-06-22 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0009_media_remove_video_event_alter_location_event_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="event",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="location",
                to="events.event",
            ),
        ),
    ]
