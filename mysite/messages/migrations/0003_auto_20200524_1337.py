# Generated by Django 3.0.4 on 2020-05-24 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
        ('my.messages', '0002_auto_20200524_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.Chat'),
        ),
    ]
