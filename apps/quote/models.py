from __future__ import unicode_literals
from django.db import models
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import get_messages

class UserManager(models.Manager):
    def validator(self, request):
        if len(request.POST['name']) < 1:
            messages.add_message(request, messages.ERROR, "You must enter your name")
        
        if len(request.POST['email']) < 1:
            messages.add_message(request, messages.ERROR, "You have to enter an email")
        try:
            user = User.objects.filter(email = request.POST['email'])
            if len(user) > 0:   
                messages.add_message(request, messages.ERROR, "You are already registred")
                return False
        except:
            messages.add_message(request, messages.ERROR, "You are already registred")
            return False
        if len(request.POST['alias']) < 1:
             messages.add_message(request, messages.ERROR, "You must enter alias")
        if len(request.POST['password']) < 8:
             messages.add_message(request, messages.ERROR, "Password must be at least 8 characters.")
        if request.POST['password'] != request.POST['confirmpass']:
             messages.add_message(request, messages.ERROR, "Passwords must match")
        if request.POST['date'] > str(datetime.now()):
             messages.add_message(request, messages.ERROR, 'Date must be in the past')
        if len(get_messages(request)) > 0:
            return False
        else:
            pasw = pbkdf2_sha256.encrypt(request.POST['password'], rounds=12000, salt_size=32)

            user = User.objects.create(
                name = request.POST['name'],
                alias = request.POST['alias'],
                email=request.POST['email'],
                password = pasw,
                date = request.POST['date'])
            
            request.session['name'] = request.POST['name']
            request.session['user_id'] = user.id
            
            return True

    def contribute(self, request):
        if len(request.POST['quoted']) < 3:
             messages.add_message(request, messages.ERROR, 'You must enter who quoted')
        
        if len(request.POST['qmessage']) < 10:
             messages.add_message(request, messages.ERROR, 'Your message must contain at least 10 caracters')
        
        if len(get_messages(request)) > 0:
            return False
        else:
            user = User.objects.get(id = request.session['user_id'])
            Quotable.objects.create(
                description = request.POST['qmessage'],
                quoted_by = request.POST['quoted'],
                user_quotes = user,
            )
            return True

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length = 255)
    date = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Quotable(models.Model):
    description = models.TextField()
    quoted_by = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    users_liked = models.ManyToManyField(User, related_name = "favorite_quote")
    user_quotes = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'quote')
    objects = UserManager()
