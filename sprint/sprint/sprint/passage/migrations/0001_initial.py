# Generated by Django 4.2.13 on 2024-07-01 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(verbose_name='Широта')),
                ('longitude', models.FloatField(verbose_name='Долгота')),
                ('height', models.IntegerField(verbose_name='Высота')),
            ],
            options={
                'verbose_name': 'Координаты',
            },
        ),
        migrations.CreateModel(
            name='Levels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winter', models.CharField(blank=True, choices=[('-', '-'), ('1a', '1A'), ('1b', '1Б'), ('2a', '2А'), ('2b', '2Б'), ('3a', '3А'), ('3b', '3Б'), ('3b+', '3Б+')], max_length=3, null=True, verbose_name='Зима')),
                ('spring', models.CharField(blank=True, choices=[('-', '-'), ('1a', '1A'), ('1b', '1Б'), ('2a', '2А'), ('2b', '2Б'), ('3a', '3А'), ('3b', '3Б'), ('3b+', '3Б+')], max_length=3, null=True, verbose_name='Зима')),
                ('summer', models.CharField(blank=True, choices=[('-', '-'), ('1a', '1A'), ('1b', '1Б'), ('2a', '2А'), ('2b', '2Б'), ('3a', '3А'), ('3b', '3Б'), ('3b+', '3Б+')], max_length=3, null=True, verbose_name='Зима')),
                ('autumn', models.CharField(blank=True, choices=[('-', '-'), ('1a', '1A'), ('1b', '1Б'), ('2a', '2А'), ('2b', '2Б'), ('3a', '3А'), ('3b', '3Б'), ('3b+', '3Б+')], max_length=3, null=True, verbose_name='Зима')),
            ],
            options={
                'verbose_name': 'Уровень сложности',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('fam', models.TextField(max_length=30, verbose_name='Фамилия')),
                ('name', models.TextField(max_length=30, verbose_name='Имя')),
                ('otc', models.TextField(max_length=30, verbose_name='Отчество')),
                ('phone', models.CharField(max_length=30, verbose_name='Номер телефона')),
            ],
            options={
                'verbose_name': 'Турист',
            },
        ),
        migrations.CreateModel(
            name='Passage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beauty_title', models.TextField(blank=True, null=True, verbose_name='Название')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название вершины')),
                ('other_titles', models.CharField(blank=True, max_length=100, null=True, verbose_name='Другие названия')),
                ('connect', models.TextField(blank=True, null=True, verbose_name='Что соединяет')),
                ('add_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('coordinates', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passage.coordinates')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passage.levels')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passage.users')),
            ],
        ),
    ]