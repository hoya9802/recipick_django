# Generated by Django 3.2.25 on 2024-12-11 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20241211_0141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='sender_id',
            new_name='sender_nick_name',
        ),
    ]