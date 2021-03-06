# Generated by Django 4.0.5 on 2022-06-21 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_alter_event_summary_alter_event_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="loc_type",
        ),
        migrations.RemoveField(
            model_name="event",
            name="location",
        ),
        migrations.AlterField(
            model_name="event",
            name="description",
            field=models.TextField(
                blank=True, max_length=2500, null=True, verbose_name="description"
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=5,
                max_digits=22,
                null=True,
                verbose_name="price",
            ),
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "location_type",
                    models.CharField(
                        choices=[
                            ("Venue", "Venue"),
                            ("Online", "Online"),
                            ("To Be Announced", "Tba"),
                        ],
                        default="Venue",
                        max_length=100,
                        verbose_name="location_type",
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True, max_length=1500, null=True, verbose_name="location"
                    ),
                ),
                (
                    "conference_uri",
                    models.URLField(
                        blank=True, null=True, verbose_name="conference_uri"
                    ),
                ),
                (
                    "lat",
                    models.DecimalField(
                        blank=True,
                        decimal_places=16,
                        max_digits=22,
                        null=True,
                        verbose_name="lat",
                    ),
                ),
                (
                    "long",
                    models.DecimalField(
                        blank=True,
                        decimal_places=16,
                        max_digits=22,
                        null=True,
                        verbose_name="long",
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="state"
                    ),
                ),
                (
                    "event",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="location",
                        to="events.event",
                    ),
                ),
            ],
        ),
    ]
