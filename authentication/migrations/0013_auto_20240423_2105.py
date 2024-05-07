# Generated by Django 3.2.7 on 2024-04-23 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_card_penalty'),
    ]

    operations = [
        migrations.CreateModel(
            name='PC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_number', models.IntegerField(unique=True)),
                ('team1_name', models.CharField(max_length=100)),
                ('team2_name', models.CharField(max_length=100)),
                ('team1_pc', models.IntegerField(default=0)),
                ('team2_pc', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_number', models.IntegerField(unique=True)),
                ('team1_name', models.CharField(max_length=100)),
                ('team2_name', models.CharField(max_length=100)),
                ('team1_ps', models.IntegerField(default=0)),
                ('team2_ps', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='Penalty',
        ),
    ]
