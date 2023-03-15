# Generated by Django 4.1.5 on 2023-01-28 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionListings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField(max_length=500)),
                ('starting_bid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image_url', models.TextField()),
                ('category', models.CharField(max_length=100)),
            ],
        ),
    ]