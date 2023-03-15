from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("categories", views.categories, name="categories"),
    path(
        "categories/<str:category_name>",
        views.category_products,
        name="category_products",
    ),
]
