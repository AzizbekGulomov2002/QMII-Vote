# Generated by Django 3.2.1 on 2024-02-09 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('total_vote', models.IntegerField(default=0)),
                ('voters', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Kafedra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voteapp.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start', models.DateField()),
                ('finish', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='images')),
                ('name', models.CharField(max_length=200)),
                ('work_year', models.DateField()),
                ('stuff', models.CharField(max_length=200)),
                ('kafedra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voteapp.kafedra')),
            ],
        ),
        migrations.AddField(
            model_name='faculty',
            name='vote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voteapp.vote'),
        ),
        migrations.CreateModel(
            name='CategoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('total_vote', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='voteapp.category')),
                ('voters', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
