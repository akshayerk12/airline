# Generated by Django 4.2.6 on 2023-11-09 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('llmapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='airline',
            old_name='From',
            new_name='From_location',
        ),
        migrations.RenameField(
            model_name='airline',
            old_name='To',
            new_name='To_location',
        ),
    ]