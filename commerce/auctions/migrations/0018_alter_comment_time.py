# Generated by Django 4.1.5 on 2023-02-08 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_remove_bid_time_comment_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
