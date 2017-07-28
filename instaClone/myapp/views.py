# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from models import User, SessionToken, Post, Like, Comment
from django.contrib.auth.hashers import make_password,check_password
import datetime
from imgurpython import ImgurClient
from instaClone.settings import BASE_DIR
from Clarify import get_tags_from_image
from sendgrid_email import send_response
from enum import Enum
from PIL import Image
from django.utils import timezone


# Create your views here.


def signup_view(request):
    response_data = {}
    today = datetime.date.today()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if len(username) < 4:
                response_data['msg'] = 'Username should have atleast 4 characters'
            if len(password) < 5:
                response_data['msg'] = 'Password should have atleast 5 characters'

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
        posts = Post.objects.all().order_by('-created_on')
        for post in posts:
            existing_like = Like.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True
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
                main, sub = image.content_type.split('/')
                if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
                    form = PostForm()
                    message = {'message': 'Enter JPEG or PNG image', 'form': form}
                    return render(request, 'post.html', message)
                else:
                    caption = form.cleaned_data.get('caption')
                    post = Post(user=user, image=image, caption=caption)
                    post.save()

                    path = str(BASE_DIR + '/' + post.image.url)

                    client = ImgurClient('e9d9aee5f532f88', '8d0e8bb5ef8ccd95533624535c279c687423b754')
                    post.image_url = client.upload_from_path(path, anon=True)['link']
                    response_clarifai = get_tags_from_image(post.image_url)
                    print response_clarifai
                    arr_of_dict = response_clarifai['outputs'][0]['data']['concepts']
                    for i in range(0, len(arr_of_dict)):
                        keyword = arr_of_dict[i]['name']
                        value = arr_of_dict[i]['value']
                        if (keyword == 'Dirty' and value > 0.5):
                            is_dirty = True
                            send_response(post.image_url)

                        elif (keyword == 'Clean' and value > 0.5):
                            is_dirty = False
                        else:
                            is_dirty = False
                    post.is_dirty = is_dirty

                    post.save()
                    return redirect('/feed/')
        else:
            print request.body
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')


def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = Like.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                Like.objects.create(post_id=post_id, user=user)
                print 'Liked Post'
            else:
                existing_like.delete()
                print "Unliked"

            return redirect('/feed/')

    else:
        return redirect('/login/')


def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = Comment.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            print 'commented'
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')


def logout_view(request):
    user = check_validation(request)
    if user is not None:
        latest_session = SessionToken.objects.filter(user=user).last()
        if latest_session:
            latest_session.delete()

    return redirect("/login/")


# for session validation

def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
        return None
