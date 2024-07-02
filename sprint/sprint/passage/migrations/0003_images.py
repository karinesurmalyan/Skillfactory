# Generated by Django 4.2.13 on 2024-07-01 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('passage', '0002_passage_status_alter_passage_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.URLField(blank=True)),
                ('title', models.TextField(blank=True, max_length=255, null=True)),
                ('passage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='passage.passage')),
            ],
        ),
    ]