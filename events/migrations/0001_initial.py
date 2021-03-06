# Generated by Django 4.0.4 on 2022-06-10 00:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Events",
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
                ("title", models.CharField(max_length=500, verbose_name="title")),
                (
                    "description",
                    models.CharField(max_length=5000, verbose_name="description"),
                ),
                ("place", models.CharField(max_length=500, verbose_name="place")),
                ("start_date", models.DateTimeField(verbose_name="start date")),
                ("end_date", models.DateTimeField(verbose_name="end date")),
                ("url", models.CharField(max_length=500, verbose_name="url")),
                (
                    "creator",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("start_date",),
            },
        ),
        migrations.CreateModel(
            name="Category",
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
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.events"
                    ),
                ),
            ],
        ),
    ]
