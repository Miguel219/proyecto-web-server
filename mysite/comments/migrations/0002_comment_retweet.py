# Generated by Django 3.0.4 on 2020-05-23 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
        ('retweets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='retweet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='retweets.Retweet'),
        ),
    ]
