from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse 
from django.forms import ModelForm # Import objects from the existing models
from .models import *
from django.utils import timezone

# New Listing
class NewListingForm(ModelForm):
    class Meta:
        # Specify which ModelForm to import from
        model = Listing
        # Specify the fields
        fields = ["title", "startingPrice", "imageURL", "description", "category"]

# Place a bid
class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['offered_price']

# Post a comment
class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


# Test
class NewCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category']

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "categories": Category.objects.all()
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def new(request):
    if request.method == "POST":
        # Create a new listing out of the data of the form
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            # commit = False is used whenever you want to get data from outside of the form
            newListing = form.save(commit=False)
            # newListing is now a "model object"
            newListing.creator = request.user
            newListing.save()

        return HttpResponseRedirect(reverse('index'))            

    else:
        return render(request, 'auctions/new_listing.html', {
            "form": NewListingForm()
        })

@login_required
def watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # if already in watchlist , remove the user
    if request.user in listing.watchers.all():
        listing.watchers.remove(request.user)
    else:
        # Add user to watchlist
        listing.watchers.add(request.user)

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


# Listing page view
@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    # Check if anyone made a bid on the listing
    if Bid.objects.filter(listing=listing):
        bid = Bid.objects.filter(listing=listing).order_by('date').last().user
    else:
        bid = None
    
        
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid": NewBidForm(),
        "comment": NewCommentForm(),
        "comments": listing.comments.all(),
        "user": request.user,
        "watchers": listing.watchers.all(),
        "last_bidder": bid 
    })


@login_required
def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        comment = NewCommentForm(request.POST)
        if comment.is_valid():
            comment = comment.save(commit=False)
            comment.user = request.user
            comment.listing = listing
            comment.save()
    
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))            


@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    offer = float(request.POST["offered_price"])
    # Validate the offer
    if (not listing.currentPrice and offer >= listing.startingPrice) or (listing.currentPrice and offer > listing.currentPrice):
        listing.currentPrice = offer
        # Create a newBidForm to keep track of all bids
        newBid = NewBidForm(request.POST)
        newBid = newBid.save(commit=False)
        newBid.user = request.user
        newBid.listing = listing
        newBid.save()
        listing.save()
        # redirect the user to listing page
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    else:
        # Check if anyone made a bid on the listing
        if Bid.objects.filter(listing=listing):
            bid = Bid.objects.filter(listing=listing).order_by('date').last().user
        else:
            bid = None
    
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid": NewBidForm(),
            "comment": NewCommentForm(),
            "comments": listing.comments.all(),
            "user": request.user,
            "watchers": listing.watchers.all(),
            "message": "Invalid Bid",
            "last_bidder": bid

        })


@login_required
def myWatchlist(request):
    # listing object
    listing = request.user.watched_items.all()
    return render(request, "auctions/index.html", {
        "listings": listing
    })

        
def activeListings(request):
    listings = Listing.objects.filter(isActive=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": Category.objects.all()
    })

def category(request, category_id):

    listings = Listing.objects.filter(category=category_id)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


@login_required
def close_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.user == listing.creator:
        listing.isActive = False
        # Get all the last bid on the listing
        # winner could be None
        winner = Bid.objects.filter(listing=listing_id).last().user
        listing.buyer = winner
        listing.save()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            
        })
        

    