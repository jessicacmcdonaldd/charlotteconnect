from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Group(models.Model):
    #host = 
    #topic = 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    #participants = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, default="Untitled")
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]
    
class Comment(models.Model):
    message = models.ForeignKey(Message, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    enrolled_courses = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"