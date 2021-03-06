# Generated by Django 3.0.4 on 2020-05-23 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tweets', '0001_initial'),
        ('users', '0002_auto_20200522_2306'),
        ('retweets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='retweet',
            name='originalTweet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tweets.Tweet'),
        ),
        migrations.AddField(
            model_name='retweet',
            name='originalUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='originalUser', to='users.User'),
        ),
        migrations.AddField(
            model_name='retweet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='users.User'),
        ),
    ]
