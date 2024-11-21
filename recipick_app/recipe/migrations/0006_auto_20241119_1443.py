# Generated by Django 3.2.25 on 2024-11-19 05:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0005_likeng'),
    ]

    operations = [
        migrations.AddField(
            model_name='likeng',
            name='create_dt',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='likeng',
            name='rate',
            field=models.SmallIntegerField(choices=[(-1, 'Dislike'), (1, 'Like')]),
        ),
        migrations.AlterField(
            model_name='likeng',
            name='rater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='likeng',
            name='recipe_rated',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='recipe.recipe'),
        ),
    ]