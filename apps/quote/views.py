
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quotable
import timeit
from passlib.hash import pbkdf2_sha256
from django.contrib import messages
from django.contrib.messages import get_messages


def index(request):
    return render(request, 'index.html')

def tohome(request):
    return redirect('/main')

def login(request):
    try:
        user = User.objects.get(email = request.POST['email'])
        if pbkdf2_sha256.verify(request.POST['password'], user.password):

            request.session['name'] = user.name
            request.session['user_id'] = user.id
            return redirect("/quotes")
        else:
            messages.add_message(request, messages.ERROR, "Wrong password provided")
    except: 
        messages.add_message(request, messages.ERROR, "No such user in our database try to create an account")
        return redirect('/')
    
def new_user(request):
    errors = User.objects.validator(request)
    if errors:
        return redirect('/')
    else:
        return redirect('/quotes')
    

def logout(request):
    request.session.flush()
    return redirect('/')

def quotes(request):
    if not 'user_id' in request.session:
        messages.add_message(request, messages.ERROR, 'You need to log in or register first')
        return redirect('/')

    user = User.objects.get(id = request.session['user_id'])

    all_quotes = Quotable.objects.all()

    fav_quotes = Quotable.objects.filter(users_liked = user) | Quotable.objects.filter(user_quotes = user)
    other = []
    for quote in all_quotes:
        if not quote in fav_quotes:
            other.append(quote)

    print(fav_quotes)
    print (other)

    context = {
        'fav_quotes' : fav_quotes,
        'other_quotes' : other,
        'all' : all_quotes
    }
    return render(request, 'all_quotes.html', context)

def display(request, id):

    user = User.objects.get(id = id)
    all_q =  Quotable.objects.filter(user_quotes = user)
    counter = len(all_q)
    context ={
        'quotes' : all_q,
        'user' : user.name,
        'count' : counter
    }
    return render(request, 'display.html', context)

def remove_fav(request, id):
    user = User.objects.get(id = request.session['user_id'])
    quote = Quotable.objects.get(id = id)
    quote.users_liked.remove(user)
    return redirect('/quotes')
    # .Remove

def add_fav(request, id):
    user = User.objects.get(id = request.session['user_id'])
    quote =  Quotable.objects.get(id = id)
    quote.users_liked.add(user)
    return redirect("/quotes")

def newquote(request):
    if Quotable.objects.contribute(request):
        return(redirect("/quotes"))
    else:
        return(redirect("/quotes"))