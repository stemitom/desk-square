# Generated by Django 4.0.5 on 2022-06-21 00:32

import datetime
import django.core.validators
from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0004_etype_alter_category_event_delete_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                    "name",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Tags can only contain letters, numbers and underscores",
                                regex="^[A-Za-z0-9_]+$",
                            )
                        ],
                        verbose_name="tag",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="etype",
            name="event",
        ),
        migrations.RemoveField(
            model_name="location",
            name="event",
        ),
        migrations.RemoveField(
            model_name="time",
            name="event",
        ),
        migrations.AddField(
            model_name="event",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Auto, Boat & Air", "Auto"),
                    ("Business and Professional", "Business"),
                    ("Charity & Causes", "Charity"),
                    ("Community", "Community"),
                    ("Family & Education", "Family"),
                    ("Fashion & Beauty", "Fashion"),
                    ("Film & Entertainment", "Film"),
                    ("Food & Drink", "Food"),
                    ("Fair", "Fair"),
                    ("Technology", "Tech"),
                    ("Category", "Category"),
                ],
                max_length=1500,
                null=True,
                verbose_name="category",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="end_date",
            field=models.DateField(
                default=datetime.date.today, verbose_name="end date"
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="end_time",
            field=models.TimeField(blank=True, null=True, verbose_name="end_time"),
        ),
        migrations.AddField(
            model_name="event",
            name="event_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Appearance & Signing", "Appearance"),
                    ("Attraction", "Attraction"),
                    ("Camp, Trip and Retreat", "Camp"),
                    ("Concert Performance", "Concert"),
                    ("Conference", "Conference"),
                    ("Convention", "Convention"),
                    ("Dinner or Gala", "Dinner"),
                    ("Festival or Fair", "Festival"),
                    ("Game or Competition", "Game"),
                    ("Meeting or Network Events", "Meeting"),
                    ("Other", "Other"),
                    ("Party or Social Gathering", "Party"),
                    ("Race or Endurance Event", "Race"),
                    ("Rally", "Rally"),
                    ("Screening", "Screening"),
                    ("Seminar", "Seminar"),
                    ("Tour", "Tour"),
                    ("Tradeshow or Expo", "Tradeshow"),
                    ("Type", "Type"),
                ],
                max_length=100,
                null=True,
                verbose_name="type",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="loc_type",
            field=models.CharField(
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
        migrations.AddField(
            model_name="event",
            name="location",
            field=models.CharField(
                blank=True, max_length=1500, null=True, verbose_name="location"
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="start_date",
            field=models.DateField(
                default=datetime.date.today, verbose_name="start date"
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="start_time",
            field=models.TimeField(blank=True, null=True, verbose_name="start_time"),
        ),
        migrations.AddField(
            model_name="event",
            name="timing_type",
            field=models.CharField(
                choices=[("Single Event", "Single"), ("Recurring Event", "Recurring")],
                default="Single Event",
                max_length=100,
                verbose_name="timing_type",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="tz",
            field=timezone_field.fields.TimeZoneField(
                choices_display="WITH_GMT_OFFSET", default="Africa/Lagos"
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="description",
            field=models.CharField(
                blank=True, max_length=2500, null=True, verbose_name="description"
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="title",
            field=models.CharField(db_index=True, max_length=100, verbose_name="title"),
        ),
        migrations.AlterField(
            model_name="event",
            name="url",
            field=models.CharField(
                blank=True, max_length=500, null=True, verbose_name="url"
            ),
        ),
        migrations.DeleteModel(
            name="Category",
        ),
        migrations.DeleteModel(
            name="EType",
        ),
        migrations.DeleteModel(
            name="Location",
        ),
        migrations.DeleteModel(
            name="Time",
        ),
        migrations.AddField(
            model_name="tag",
            name="event",
            field=models.ManyToManyField(related_name="tags", to="events.event"),
        ),
    ]
