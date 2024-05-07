# Generated by Django 3.2.7 on 2024-04-18 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_goal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goal',
            old_name='fg',
            new_name='FG',
        ),
        migrations.RenameField(
            model_name='goal',
            old_name='pg',
            new_name='PG',
        ),
        migrations.AlterField(
            model_name='goal',
            name='team1_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='goal',
            name='team2_name',
            field=models.CharField(max_length=255),
        ),
    ]
