# Generated by Django 3.2.25 on 2024-11-20 06:50

from django.db import migrations, models
import recipe.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_auto_20241119_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(null=True, upload_to=recipe.models.recipe_image_file_path),
        ),
    ]
