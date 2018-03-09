# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt 

NAME_REGEX = re.compile(r"^[a-zA-Z-' ]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
PASS_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+$")

class LangManager(models.Manager):
    def lang_valid(self, post_data): 
        errors = []

        if len(post_data['lang1']) < 1:
            errors.append("You must enter text for the Source Language!")
        if len(post_data['lang2']) < 1:
            errors.append("You must enter text for the Translated Language!")
        
        if len(errors) > 0:
            return (False, errors) 
        else:
            lang1 = Lang1.objects.create(
                text1 = post_data['lang1'],
            )
            lang2 = Lang2.objects.create(
                text2 = post_data['lang2'],
                translation = Lang1.objects.get(id=lang1.id)
            )
            return (True, lang1, lang2)

    def lang_edit(self, post_data, text_id): 
        errors = []

        if len(post_data['lang1']) < 1:
            errors.append("You must enter text for the Source Language!")
        if len(post_data['lang2']) < 1:
            errors.append("You must enter text for the Translated Language!")
        
        if len(errors) > 0:
            return (False, errors) 
        else:
            lang1 = Lang1.objects.get(id=text_id)
            lang1.text1 = post_data['lang1']
            lang1.save()
            lang2 = Lang2.objects.get(id=text_id)
            lang2.text2 = post_data['lang2']
            lang2.save()
            return (True, lang1, lang2)

class Lang1(models.Model):
    text1 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LangManager()

class Lang2(models.Model):
    text2 = models.TextField()
    translation = models.OneToOneField(Lang1, related_name="source")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LangManager()

class UserManager(models.Manager):
    def signup(self, post_data):
        errors = []
        if len(post_data['first']) < 1:
            errors.append("First Name cannot be left blank!")
        elif len(post_data['first']) < 2:
            errors.append("First Name must be at least 2 characters long")
        if not NAME_REGEX.match(post_data['first']):
            errors.append("Invalid characters in First Name")

        if len(post_data['last']) < 1:
            errors.append("Last Name cannot be left blank!")
        elif len(post_data['last']) < 2:
            errors.append("Last Name must be at least 2 characters long")
        if not NAME_REGEX.match(post_data['last']):
            errors.append("Invalid characters in Last Name")

        if len(post_data['email']) < 1:
            errors.append("Email cannot be left blank!")
        elif not EMAIL_REGEX.match(post_data['email']):
            errors.append("Invalid characters in email")
        check_email = User.objects.filter(email = post_data['email'])
        if len(check_email) > 0:
            errors.append("Email already exists")

        if len(post_data['password']) < 1:
            errors.append("Password cannot be left blank!")
        elif len(post_data['password']) < 8:
            errors.append("Password should be at least 8 characters")
        if not PASS_REGEX.match(post_data['password']):
            errors.append("Invalid characters in Password")
        if post_data['password'] != post_data['confirm']:
            errors.append("Passwords do not match!")
                
        if len(errors) > 0:
            return (False, errors)
        else: 
            user = User.objects.create(
                first_name = post_data['first'],
                last_name = post_data['last'],
                email = post_data['email'],
                password = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt()),
                level = 0
            )
            if user.id == 1:
                user.level = 9
                user.save()
            else:
                user.level = post_data['level']
                user.save()
            return(True, user)

    def login(self, post_data):
        errors = []

        if len(post_data['password']) < 1:
            errors.append("Password cannot be left blank!")
        elif len(post_data['password']) < 8:
            errors.append("Password should be at least 8 characters")
        if not PASS_REGEX.match(post_data['password']):
            errors.append("Invalid characters in Password")

        if len(post_data['email']) < 1:
            errors.append("Email cannot be left blank!")
        if not EMAIL_REGEX.match(post_data['email']):
            errors.append("Invalid characters in email")
        check_email = User.objects.filter(email = post_data['email'])
        if len(check_email) == 0:
            errors.append("Email does not exist")

        else:
            user = check_email[0]
            if not bcrypt.checkpw(post_data["password"].encode(), user.password.encode()):
                errors.append("Invalid Password")

            if len(errors) > 0:
                return (False, errors)
            else: 
                return(True, user)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    level = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
