from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.postgres.fields import JSONField 
import json
from django.contrib.auth import get_user_model


# Create your models here.


class Genre(models.Model):

    name = models.CharField(max_length=30, unique=True)
    colour = models.CharField(max_length=255, unique=False, default='#41ceaa')

    def __str__(self):
        return self.name
    
class User(AbstractUser):

    online_id = models.CharField(max_length=255, unique=True)
    favourite_genres = models.ManyToManyField(Genre, blank=True)
    favourite_books= models.JSONField(default=list, blank=True)
    DOB = models.DateField(null=True,blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name = "custom_user_set",
        blank = True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name = "custom_user_permissions_set",
        blank = True
    )

    def get_genres(self):
        return [[x.name,x.colour] for x in self.favourite_genres.all()]
    
    def to_dict(self):
        return {
            'id' : self.id,
            'username': self.username,
            'online_id': self.online_id,
            'DOB': self.DOB,
            'favourite_genres': self.get_genres(),
            'favourite_books': self.favourite_books
        }
    
    def user_list_to_dict(self):
        return {
            'id': self.id,
            'online_id': self.online_id,
            'favourite_genres': self.get_genres(),
            'is_friend': False
        }
    def user_list_friend_to_dict(self):
        return {
            'id': self.id,
            'online_id': self.online_id,
            'favourite_genres': self.get_genres(),
            'favourite_books': self.favourite_books,
            'is_friend': True
        }
    

class BookRating(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book_id = models.CharField(max_length=255)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.user.id} - {self.book_id} - {self.rating}"

class Friendship(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="logged_user")
    friend = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="friends_of_logged_user")

    class Meta:
        unique_together = ('user','friend')
    
    def get_friend(self):
        return {
            "friend_id" : self.friend.id
        }

class FriendRequest(models.Model):

    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="sender")
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reciever")
    status = models.CharField(max_length=10, choices=[('pending','Pending'),('accepted','Accepted'),('declined','Declined')], default='pending')

    class Meta:
        unique_together = ('from_user','to_user')
    
    def to_dict_recieved(self):
        return {
            'id' : self.id,
            'from_user_online_id': self.from_user.online_id,
            'status': self.status,
            'type' : "incoming request"
        }
    
    def to_dict_sent(self):
        return {
            'id' : self.id,
            'to_user_online_id': self.to_user.online_id,
            'status': self.status,
            'type' : "outgoing request"
        }


