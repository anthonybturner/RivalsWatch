# Generated by Django 5.1.6 on 2025-03-20 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_matchhistory_disconnected"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="matchhistory",
            name="match_player",
        ),
    ]
