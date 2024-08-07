# Generated by Django 4.2.13 on 2024-07-01 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('passage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='passage',
            name='status',
            field=models.CharField(choices=[('new', 'новый'), ('pending', 'в работе'), ('accepted', 'принят'), ('rejected', 'отклонен')], default='new', max_length=8),
        ),
        migrations.AlterField(
            model_name='passage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='passage.users'),
        ),
    ]
