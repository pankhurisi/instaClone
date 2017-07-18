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
    create_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class SessionToken(models.Model):
    user = models.ForeignKey(User)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = uuid.uuid4()
