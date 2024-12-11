# Generated by Django 3.2.25 on 2024-12-10 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('shop_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_chatrooms', to=settings.AUTH_USER_MODEL)),
                ('visitor_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitor_chatrooms', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('shop_user', 'visitor_user')},
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_email', models.EmailField(max_length=254)),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chatroom')),
            ],
        ),
    ]