# Generated by Django 3.2.25 on 2024-11-18 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportpage',
            old_name='link',
            new_name='url',
        ),
    ]