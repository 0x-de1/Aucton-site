# Generated by Django 4.1.5 on 2023-02-07 17:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_auctionlisting_listing_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='time',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
