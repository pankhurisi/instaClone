# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, PostForm
from models import User, SessionToken,Post
from django.contrib.auth.hashers import make_password,check_password
import datetime
from imgurpython import ImgurClient
from instaClone.settings import BASE_DIR
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
            user = User(name=name, password=make_password(password), email=email, username=username)
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
            else:
                response_data['message'] = 'Incorrect Username! enter again'

    elif request.method == "GET":
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)


def feed_view(request):
    user = check_validation(request)
    if user:
        posts = Post.objects.all().order_by('created_on')
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')


def post_view(request):
    user = check_validation(request)
    if user:
        if request.method == 'GET':
            form = PostForm()
        elif request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = Post(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + '//user_images//post.image.url')

                client = ImgurClient('e9d9aee5f532f88', '8d0e8bb5ef8ccd95533624535c279c687423b754')
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()
                return redirect('/feed/')
            else:
                form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')


# for session validation

def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
        return None
