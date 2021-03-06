# Generated by Django 4.0.5 on 2022-06-20 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0003_event_image_location_ticket_time_type_video_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="EType",
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
                    "etype",
                    models.CharField(
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
                (
                    "event",
                    models.ManyToManyField(related_name="etype", to="events.event"),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="category",
            name="event",
            field=models.ManyToManyField(related_name="category", to="events.event"),
        ),
        migrations.DeleteModel(
            name="Type",
        ),
    ]
