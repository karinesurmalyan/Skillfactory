# Generated by Django 4.2.11 on 2024-04-10 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('A', 'Статья'), ('N', 'Новость')], default='N', max_length=1),
        ),
    ]
