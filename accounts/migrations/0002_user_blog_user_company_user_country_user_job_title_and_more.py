# Generated by Django 4.0.5 on 2022-06-15 14:05

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="blog",
            field=models.URLField(
                blank=True, max_length=100, null=True, verbose_name="blog"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="company",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="company"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="country",
            field=django_countries.fields.CountryField(
                blank=True, max_length=2, null=True, verbose_name="country"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="job_title",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="job_title"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.IntegerField(blank=True, null=True, verbose_name="phone"),
        ),
        migrations.AddField(
            model_name="user",
            name="postal_code",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="postal_code"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="prefix",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Mrs.", "Mrs"),
                    ("Mr.", "Mr"),
                    ("Ms.", "Ms"),
                    ("Miss.", "Miss"),
                    ("Mx.", "Mx"),
                    ("Dr.", "Dr"),
                    ("Prof.", "Prof"),
                    ("Rev.", "Rev"),
                ],
                max_length=20,
                null=True,
                verbose_name="prefix",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="website",
            field=models.URLField(
                blank=True, max_length=100, null=True, verbose_name="website"
            ),
        ),
    ]
