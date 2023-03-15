from django.contrib import admin
from .models import AuctionListing, Comment, Bid, User


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "id",
        "short_description",
        "starting_bid",
        "image_url",
        "category",
        "listing_status",
        "owner",
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "listing",
        "comment",
        "time",
    )


# Register your models here.
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User)
