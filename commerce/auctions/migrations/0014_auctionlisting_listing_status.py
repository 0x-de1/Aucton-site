# Generated by Django 4.1.5 on 2023-02-06 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_auctionlisting_watchlist_user_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='listing_status',
            field=models.BooleanField(default=False),
        ),
    ]