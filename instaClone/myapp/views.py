# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from forms import SignUpForm
from models import User
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password


# Create your views here.


def signup_view(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST":
        print 'Sign up form submitted'
    elif request.method == 'GET':
        form = SignUpForm()
    return render(request, 'index.html', {'form': form})
