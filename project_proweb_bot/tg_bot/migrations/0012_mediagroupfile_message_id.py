# Generated by Django 5.1.7 on 2025-04-02 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0011_postinchat'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediagroupfile',
            name='message_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Тг ид сообщения'),
        ),
    ]
