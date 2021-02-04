from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	pass
	# displayName = models.CharField(max_length=64)
	# username = models.CharField(max_length=20, unique=True)
	# password = models.CharField(max_length=16)

class AuctionListing(models.Model):
	FASHION = "F"
	TOYS = "T"
	ELECTRONICS = "E"
	HOME = "H"
	GENERAL = "G"

	CATEGORY_CHOICES = [
		(FASHION, "Fashion"),
		(TOYS, "Toys"),
		(ELECTRONICS, "Electronics"),
		(HOME, "Home"),
		(GENERAL, "General")
	]

	title = models.CharField(max_length=50)
	description = models.CharField(max_length=256)
	startingBid = models.FloatField()
	imageURL = models.CharField(default="", max_length=100)
	isActive = models.BooleanField(default=True)
	auctioner = models.ForeignKey(User, on_delete=models.CASCADE)

	category = models.CharField(
		default=GENERAL,
		max_length=15,
		choices=CATEGORY_CHOICES
	)

class Bid(models.Model):
	listing = models.ForeignKey(AuctionListing, models.CASCADE)
	bidder = models.ForeignKey(User, on_delete=models.CASCADE)
	bidAmount = models.FloatField()

class Comment(models.Model):
	comment = models.CharField(max_length=120)
	listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
	commenter = models.ForeignKey(User, on_delete=models.CASCADE)
