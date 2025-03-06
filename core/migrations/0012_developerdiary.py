# Generated by Django 5.1.6 on 2025-03-06 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_alter_ability_damage"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeveloperDiary",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                ("date", models.DateField(auto_now_add=True)),
                ("overview", models.TextField()),
                ("image_path", models.CharField(max_length=200)),
                ("full_content", models.TextField()),
            ],
        ),
    ]
