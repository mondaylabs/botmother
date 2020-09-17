# Generated by Django 3.0.5 on 2020-09-15 12:53

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.BigIntegerField()),
                ('type', models.CharField(max_length=255)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_action', models.CharField(max_length=255, null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('last_activity', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'telegram_chats',
            },
        ),
        migrations.CreateModel(
            name='Push',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('image_token', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'telegram_push_campaigns',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('date', models.DateTimeField()),
                ('text', models.TextField(blank=True, null=True, verbose_name='text')),
                ('type', models.CharField(default='text', max_length=255)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='botmother.Chat')),
            ],
            options={
                'db_table': 'telegram_messages',
            },
        ),
    ]
