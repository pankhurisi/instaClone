# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db import models
import uuid
# Create your models here.


class User(models.Model):
    email = models.EmailField(default="Ananymous")
    name = models.CharField(max_length=120, default="Ananymous")
    username = models.CharField(max_length=120, default="Ananymous")
    password = models.CharField(max_length=40, default="Ananymous")
    # updated only when the creation takes place
    create_on = models.DateTimeField(auto_now_add=True)
    # updated every time there's a change
    updated_on = models.DateTimeField(auto_now=True)


class SessionToken(models.Model):
    # userid is taken as foreign key
    user = models.ForeignKey(User)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = uuid.uuid4()


class Post(models.Model):
    user = models.ForeignKey(User)
    #the folder where image is saved
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    liked_by_user = False

    @property
    def like_count(self):
        return len(Like.objects.filter(post=self))

    @property
    def comments(self):
        return Comment.objects.filter(post=self).order_by('created_on')


class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    # one upvote is for each comment
    comment_text = models.CharField(max_length=555)
    upvote_number = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)