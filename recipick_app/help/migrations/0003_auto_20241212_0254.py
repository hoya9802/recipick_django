# Generated by Django 3.2.25 on 2024-12-11 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0002_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created_at',
            new_name='create_dt',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='updated_at',
            new_name='modify_dt',
        ),
    ]