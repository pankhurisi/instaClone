# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db import models
# Create your models here.


class User(models.Model):
    email = models.EmailField(default="Ananymous")
    name = models.CharField(max_length=120, default="Ananymous")
    username = models.CharField(max_length=120, default="Ananymous")
    password = models.CharField(max_length=40, default="Ananymous")
    create_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
