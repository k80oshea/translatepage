# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import Lang1, Lang2, User
from django.contrib import messages

def home(request):
    if 'email' in request.session: 
        data = {
            "users": User.objects.all(),
            "user": User.objects.get(email=request.session['email']),
            "l1_text": Lang1.objects.all(),
            "l2_text": Lang2.objects.all()
        }
    else: 
        data = {
            "l1_text": Lang1.objects.all(),
            "l2_text": Lang2.objects.all()
        }
    users = User.objects.all()
    for x in users:
        print x.first_name
        print x.level
        print type(x.level)
    if 'language' not in request.session:
        request.session['language'] = 1
    return render(request, 'translate_app/home.html', data)

def change_lang(request, lang):
    showlang = int(lang)
    request.session['language'] = showlang
    request.session.modified = True
    return redirect('/')

def login_page(request):
    data = {
        "staff": User.objects.all(),
        "numstaff": len(User.objects.all())
    }
    return render(request, 'translate_app/login.html', data)

def signup(request):
    signup_info = User.objects.signup(request.POST)
    user_list = User.objects.all()
    if signup_info[0]: 
        if(request.session['level'] == 9):
            return redirect('/')
        else:
            request.session['email'] = signup_info[1].email
            request.session['level'] = signup_info[1].level
            return redirect('/')
    else: 
        for error in signup_info[1]:
            messages.add_message(request, messages.ERROR, error)
        if(len(user_list) > 1):            
           return redirect('/newuser')
        else:
            return redirect('/login')

def add_user(request):
    if 'level' not in request.session: 
        return redirect('/')
    if request.session['level'] != 9:
        return redirect('/')
    return render(request, 'translate_app/newuser.html')
        
def admin_add(request):
    signup_info = User.objects.signup(request.POST)
    if signup_info[0]: 
        return redirect('/')
    else: 
        for error in signup_info[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/newuser')

def login(request):
    login_info = User.objects.login(request.POST)
    if login_info[0]: 
        request.session['email'] = login_info[1].email
        request.session['level'] = login_info[1].level
        return redirect('/')
    else: 
        for error in login_info[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/login')


def make_changes(request):
    if 'level' not in request.session: 
        return redirect('/')
    if request.session['level'] != 9:
        return redirect('/')
    data = {
        "user": User.objects.get(email=request.session['email']),
        "l1_text": Lang1.objects.all(),
        "l2_text": Lang2.objects.all()
    }
    return render(request, 'translate_app/admin.html', data)

def add_lang(request):
    lang_info = Lang2.objects.lang_valid(request.POST)
    if lang_info[0]: 
        return redirect('/edit/langs')
    else: 
        for error in lang_info[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/edit/langs')

def edit(request, text_id):
    if 'level' not in request.session: 
        return redirect('/')
    if request.session['level'] != 9:
        return redirect('/')
    data = {
        "l1_text": Lang1.objects.get(id=text_id),
        "l2_text": Lang2.objects.get(id=text_id)
    }
    return render(request, 'translate_app/edit.html', data)

def change(request, text_id):
    addtext_info = Lang2.objects.lang_edit(request.POST, text_id)
    if addtext_info[0]: 
        return redirect('/edit/langs')
    else: 
        for error in addtext_info[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/edit/langs')

def delete(request, text_id):
    pass

def logout(request):
    request.session.clear()
    return redirect('/')