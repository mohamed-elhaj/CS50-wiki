from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new, name="new_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("watchlist", views.myWatchlist, name="my_watchlist"),
    path("active", views.activeListings, name="active_listings"),
    path("category/<int:category_id>", views.category, name="category"),
    path("close/<int:listing_id>", views.close_bid, name="close_bid")
]
