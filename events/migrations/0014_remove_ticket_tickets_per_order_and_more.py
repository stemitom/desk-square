# Generated by Django 4.0.5 on 2022-06-29 23:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_attendee_rename_quantity_ticket_quantity_available_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='tickets_per_order',
        ),
        migrations.AddField(
            model_name='ticket',
            name='max_tickets_per_order',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='tickets_per_order'),
        ),
    ]
