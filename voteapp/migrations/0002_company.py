# Generated by Django 3.2.1 on 2024-02-07 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voteapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='images')),
            ],
        ),
    ]
