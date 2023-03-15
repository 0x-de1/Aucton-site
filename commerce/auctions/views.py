from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


from .models import User, AuctionListing, Bid, Comment
from .forms import AuctionListingForm, BidForm, CommentForm


def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings})


def category_products(request, category_name):
    listings = AuctionListing.objects.all().filter(category=category_name)
    return render(
        request,
        "auctions/category_products.html",
        {"listings": listings, "category_name": category_name},
    )


def my_watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {"listings": listings})


def categories(request):

    categories = AuctionListing.objects.values("category").distinct()
    all_listings = AuctionListing.objects.all()

    print(categories)
    listings = []
    for category_name in categories:

        print(category_name["category"])
        listing = all_listings.filter(category=category_name["category"]).first()
        print(listing)
        listings.append(listing)
    return render(request, "auctions/categories.html", {"listings": listings})


@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        try:
            listing = AuctionListing.objects.get(id=listing_id)
        except ObjectDoesNotExist:
            messages.add_message(request, messages.WARNING, "Listing does not exist")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.listing = listing
            comment.save()

        return redirect("listing", listing_id=listing_id)


@login_required
def close_auction(request, listing_id):
    if request.method == "POST":
        try:
            listing = AuctionListing.objects.get(id=listing_id)
        except ObjectDoesNotExist:
            messages.add_message(request, messages.WARNING, "Listing does not exist")
        print(request.user.id, listing.owner.id)
        if request.user.id == listing.owner.id:
            listing.listing_status = False
            listing.save()
            alert_messege = f"Listing was successfully closed."
            messages.add_message(request, messages.WARNING, alert_messege)

        return redirect("index")


@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        try:
            listing = AuctionListing.objects.get(id=listing_id)
        except ObjectDoesNotExist:
            messages.add_message(request, messages.WARNING, "Listing does not exist")

        bid_form = BidForm(request.POST)
        highest_bid = listing.highest_bid()
        starting_bid = listing.starting_bid
        bid_amount = float(request.POST.get("bid"))

        if highest_bid < bid_amount and starting_bid < bid_amount:
            if bid_form.is_valid():
                bid = bid_form.save(commit=False)
                bid.user = request.user
                bid.listing = listing
                bid.save()

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"Added your bid for ${bid_amount}",
                )
                return redirect("listing", listing_id=listing_id)

        else:
            if highest_bid < starting_bid:
                alert_messege = (
                    f"Bid must be larger than the starting bid of ${starting_bid}"
                )

            else:
                alert_messege = (
                    f"Bid must be larger than the highest bid of ${highest_bid}"
                )
            messages.add_message(request, messages.ERROR, alert_messege)

            return render(
                request,
                "auctions/bid_correction.html",
                {
                    "listing": listing,
                    "bid_form": bid_form,
                    "current_bids": listing.bids.all(),
                },
            )


def listing(request, listing_id):
    try:
        listing = AuctionListing.objects.get(id=listing_id)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.WARNING, "Listing does not exist")

    watching = None
    owner = False

    if request.user.is_authenticated:
        watching = request.user.watchlist.filter(id=listing_id)
    print(request.user.id, listing.highest_bidder())
    if not listing.listing_status and request.user.id == listing.highest_bidder():
        print("passed")
        alert_messege = f"Congratulations!! You won the bidding for this item!!"
        messages.add_message(request, messages.SUCCESS, alert_messege)

        return render(
            request,
            "auctions/closed_listing.html",
            {
                "listing": listing,
                "watching": watching,
                "current_bids": listing.bids.all(),
            },
        )

    if request.user == listing.owner:
        owner = True
    bid_form = BidForm()
    comment_form = CommentForm()
    try:
        comments = Comment.objects.all().filter(listing=listing)
    except ObjectDoesNotExist:
        comments = None
    print(comments)
    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "watching": watching,
            "bid_form": bid_form,
            "comment_form": comment_form,
            "current_bids": listing.bids.all(),
            "owner": owner,
            "comments": comments,
        },
    )


@login_required
def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        user_id = request.user.id
        listing = AuctionListing.objects.all().filter(id=listing_id).first()
        user = User.objects.all().filter(id=user_id).first()

        if listing.watching.filter(id=user_id):
            listing.watching.remove(user)
            messages.add_message(
                request, messages.WARNING, "Listing removed from your watchlist"
            )
        else:
            listing.watching.add(user)
            messages.add_message(
                request, messages.SUCCESS, "Listing added to your watchlist"
            )
        return redirect("listing", listing_id=listing_id)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def new_listing(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST)

        # Check if form data is valid (server-side)
        if not form.is_valid():
            return render(request, "auctions/new_listing.html", {"form": form})
        bid = form.save(commit=False)
        bid.owner = request.user
        bid.save()
        return redirect("index")

    form = AuctionListingForm()
    return render(request, "auctions/new_listing.html", {"form": form})
