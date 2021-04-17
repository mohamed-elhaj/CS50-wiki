from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.category}"



class Listing(models.Model):
    title = models.CharField(max_length=64)
    startingPrice = models.FloatField()
    currentPrice = models.FloatField(blank=True, null=True)
    description = models.CharField(blank=True, max_length=300)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="published_items") #User
    buyer = models.ForeignKey(User, blank=True,null=True, on_delete=models.PROTECT) #user
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_items") #User
    imageURL = models.URLField(blank=True)
    isActive = models.BooleanField(default=True)
    creationDate = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="related_items", blank=True)


    def __str__(self):
        return f"{self.title} - {self.startingPrice}$"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offered_price = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    


class Comment(models.Model):
    comment = models.CharField(max_length=300)
    creationDate = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def creation_date(self):
        return self.creationDate.strftime("%B %d %Y")

    def __str__(self):
        return f"{self.comment}"