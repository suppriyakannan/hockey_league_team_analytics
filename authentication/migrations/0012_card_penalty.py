# Generated by Django 3.2.7 on 2024-04-20 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_auto_20240420_2149'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_number', models.IntegerField(unique=True)),
                ('team1_name', models.CharField(max_length=100)),
                ('team2_name', models.CharField(max_length=100)),
                ('team1_gy', models.IntegerField(default=0)),
                ('team1_r', models.IntegerField(default=0)),
                ('team2_gy', models.IntegerField(default=0)),
                ('team2_r', models.IntegerField(default=0)),
                ('team1_total', models.IntegerField(default=0)),
                ('team2_total', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_number', models.IntegerField(unique=True)),
                ('team1_name', models.CharField(max_length=100)),
                ('team2_name', models.CharField(max_length=100)),
                ('team1_pc', models.IntegerField(default=0)),
                ('team2_pc', models.IntegerField(default=0)),
                ('team1_ps', models.IntegerField(default=0)),
                ('team2_ps', models.IntegerField(default=0)),
            ],
        ),
    ]
