# Generated by Django 5.1.6 on 2025-03-21 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_remove_matchhistory_match_player"),
    ]

    operations = [
        migrations.AddField(
            model_name="scoreinfo",
            name="match_uid",
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
