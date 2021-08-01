from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone

class User(AbstractUser):
	pass

class Listing(models.Model):
	CATEGORY_CHOICES = [
		('No category', 'No category'),
		('Toys', 'Toys'),
		('Home', 'Home'),
		('Garden', 'Garden'),
		('Books', 'Books')
	]

	title = models.CharField(max_length=100)
	description = models.CharField(max_length=30000)
	starting_bid = models.FloatField()
	current_price = models.FloatField()
	is_active = models.BooleanField(default=True)
	imageURL = models.CharField(max_length=3000, blank=True) 
	posted_date = models.DateTimeField(default=timezone.now, blank=True)

	creator = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='my_listings'
	)

	category = models.CharField(
		max_length=50,
		choices=CATEGORY_CHOICES,
		default='No category'
	) 

	watched_by = models.ManyToManyField(
		settings.AUTH_USER_MODEL,
		blank=True,
		related_name='watching'
	)

	def save(self, *args, **kwargs):
		if self.current_price is None:
			self.current_price = self.starting_bid

		super(Listing, self).save(*args, **kwargs)

class Bid(models.Model):
	bid_date = models.DateTimeField(default=timezone.now, blank=True)
	amount = models.FloatField()

	listing = models.ForeignKey(
		Listing,
		on_delete=models.CASCADE,
		related_name='l_bids'
	)

	bid_user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE, 
		related_name = 'u_bids'
	)

class Comment(models.Model):
	comment_datetime = models.DateTimeField(default=timezone.now, blank=True)
	text = models.CharField(max_length=30000)

	listing  = models.ForeignKey(
		Listing,
		on_delete=models.CASCADE,
		related_name = 'comments'
	)

	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE, 
		related_name='my_comments'
	)
