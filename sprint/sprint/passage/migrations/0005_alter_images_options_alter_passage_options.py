# Generated by Django 4.2.13 on 2024-07-02 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passage', '0004_alter_images_data_alter_levels_autumn_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='images',
            options={'verbose_name': 'Изображение', 'verbose_name_plural': 'Изображения'},
        ),
        migrations.AlterModelOptions(
            name='passage',
            options={'verbose_name': 'Перевал'},
        ),
    ]