# Generated by Django 5.1.7 on 2025-03-29 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0003_delete_postentities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_tg_id',
            field=models.CharField(max_length=455, verbose_name='Тг ид поста'),
        ),
    ]
