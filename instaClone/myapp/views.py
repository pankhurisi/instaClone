# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm
from models import User, SessionToken
from django.contrib.auth.hashers import make_password,check_password
import datetime
from django.utils import timezone


# Create your views here.


def signup_view(request):
    today = datetime.date.today()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to db
            user = User(name=name, password=make_password(password),email=email, username=username)
            user.save()
            return render(request, 'success.html', {'name': name})
        # return redirect ('login/')
        else:
            form = SignUpForm()
    elif request.method == 'GET':
        print ('Get request')
        form = SignUpForm()
    return render(request, 'index.html', {'today': today,'form': form})


def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username).first()
            if user:
                # check for the password
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! enter again'

    elif request.method == "GET":
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)


def feed_view(request):
    return render(request, 'feed.html')


# for session validation

def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
        return None
