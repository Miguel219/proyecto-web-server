# Generated by Django 3.0.4 on 2020-05-23 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retweets', '0002_auto_20200523_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='retweet',
            name='content',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
