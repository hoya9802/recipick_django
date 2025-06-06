# Generated by Django 3.2.25 on 2024-11-22 04:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import freemarket.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='freemark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to=freemarket.models.freemarket_image_file_path)),
                ('name', models.CharField(max_length=100)),
                ('purchase_dt', models.DateField()),
                ('count', models.PositiveSmallIntegerField()),
                ('is_shared', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('create_dt', models.DateField(auto_now_add=True)),
                ('modify_dt', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='freemarkets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
