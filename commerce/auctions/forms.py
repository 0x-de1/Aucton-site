from django.forms import ModelForm, TextInput
from auctions.models import AuctionListing, Bid, Comment
from django import forms

# Create the form class.
class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = "__all__"
        exclude = ["listing_status", "owner"]


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid"]


class CommentForm(ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Leave a comment here",
                "rows": 3,
                "cols": 40,
            }
        ),
        label="",
    )

    class Meta:
        model = Comment
        fields = ["comment"]
