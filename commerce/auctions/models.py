from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(AbstractUser):
    # Watchlist
    watchlist = models.ManyToManyField(
        "AuctionListing", blank=True, related_name="watching"
    )


# Auction listings
class AuctionListing(models.Model):
    # a title for the listing,
    title = models.CharField(max_length=64)
    # a text-based description,
    description = models.TextField(max_length=500)
    #  starting bid should be
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    #  URL for an image for the listing
    image_url = models.URLField(blank=True)
    #  a category (e.g. Fashion, Toys, Electronics, Home, etc.).
    category = models.CharField(max_length=100, blank=True)
    # Listing owner
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    # Listing status
    listing_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} | {self.category}"

    def short_description(self):
        three_dots = ""
        if len(self.description) > 30:
            three_dots = "..."
        return self.description[0:30].capitalize() + three_dots

    def highest_bid(self):
        if not self.bids.exists():
            return 0.0
        else:
            return self.bids.all().last().bid

    def highest_bidder(self):
        if not self.bids.exists():
            return "No bids"
        else:
            return self.bids.all().last().user.id


# Bids
class Bid(models.Model):
    # user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    # listing
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="bids"
    )
    # amount
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bid} for {self.listing} by {self.user}"

    class Meta:
        ordering = ["bid"]


# Auction listing comments
class Comment(models.Model):
    # user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    # listing
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="comments"
    )
    # comment
    comment = models.TextField(max_length=500)
    # posted time
    time = models.DateTimeField(auto_now_add=True)
