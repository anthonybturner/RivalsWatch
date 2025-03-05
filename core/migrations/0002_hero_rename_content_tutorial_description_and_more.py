# Generated by Django 5.1.6 on 2025-03-05 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image_url', models.URLField()),
            ],
        ),
        migrations.RenameField(
            model_name='tutorial',
            old_name='content',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='news',
            name='headline',
        ),
        migrations.RemoveField(
            model_name='strategy',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='tutorial',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='tutorial',
            name='youtube_link',
        ),
        migrations.AddField(
            model_name='news',
            name='title',
            field=models.CharField(default='untitled', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tutorial',
            name='url',
            field=models.URLField(default='untitled'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='strategy',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
