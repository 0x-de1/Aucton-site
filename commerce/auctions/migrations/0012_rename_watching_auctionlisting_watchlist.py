# Generated by Django 4.1.5 on 2023-02-04 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_remove_auctionlisting_watchlist_auctionlisting_owner_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='watching',
            new_name='watchlist',
        ),
    ]
