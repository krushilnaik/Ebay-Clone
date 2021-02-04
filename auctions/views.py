from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, AuctionListing

class CreateListingForm(forms.Form):
	title       = forms.CharField()
	description = forms.CharField()
	startingBid = forms.DecimalField(decimal_places=2)
	imageURL    = forms.CharField(empty_value="")



def index(request):
	return render(request, "auctions/index.html", {
		"listings": AuctionListing.objects.filter(isActive=True)
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


@login_required
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
def create_listing(request: HttpRequest):
	form = CreateListingForm(request.POST or None)
	return render(request, "auctions/create_listing.html")

@login_required
def listing(request: HttpRequest, listing_id):
	return render(request, "auctions/listing.html")

@login_required
def watchlist(request: HttpRequest):
	return render(request, "auctions/watchlist.html")

@login_required
def categories(request: HttpRequest):
	return render(request, "auctions/categories.html")
