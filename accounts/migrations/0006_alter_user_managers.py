# Generated by Django 4.0.4 on 2022-04-26 15:31

import accounts.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', accounts.managers.UserManager()),
            ],
        ),
    ]