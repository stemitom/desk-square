# Generated by Django 4.0.5 on 2022-07-26 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_alter_ticketorder_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketorder',
            name='tickets_purchased',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='events.ticket'),
        ),
        migrations.AlterField(
            model_name='ticketorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_orders', to='events.attendee'),
        ),
    ]
