# Generated by Django 2.2.2 on 2019-06-29 15:49

from django.db import migrations
import users.managers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', users.managers.CustomUserManager()),
            ],
        ),
    ]
