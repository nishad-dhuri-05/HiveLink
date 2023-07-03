from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host =models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    # if Topic class was at a lower position in this file, we would have to pass it as a string 'Topic'
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    # this means description can be blank
    description = models.TextField(null=True, blank=True)
    # blank=True means that the description attribute in form can be empty
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    #related name is used so that we dont reference a user we have already referenced in host
    # takes snapshot of the time at which the model was updated
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # newest ones will display first because of minus
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return str(self.name)


class Message(models.Model):
    # Django already makes a user model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # SET_NULL means that the messages would stay in the database even after campground is deleted
    # CASCADE means that the messages would be deleted
    body = models.TextField()
    # takes snapshot of the time at which the model was updated
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # newest ones will display first because of minus
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        # in the preview we want only the first 50 characters
        return str(self.body[0:50])
