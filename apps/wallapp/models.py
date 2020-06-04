from django.db import models
import re

class UserValidator(models.Manager):
    def registration_validator(self, data):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")
        if len(data['first_name']) <=1:
            errors['first_name'] = 'First name must be at least two characters.'
        if len(data['last_name']) <=1:
            errors['last_name'] = 'Last name must be at least two characters.'
        if len(data['password']) <=7:
            errors['password_len'] = 'Password must be at least 8 characters'
        if len(data['password']) <=1:
            errors['match'] = 'Both passwords must match.'
        if len(User.objects.filter (email=data['email'])) !=0:
            errors['email_invalid'] = 'Email is already in use'
        return errors

class MessageValidator(models.Manager):
    def basic_validator(self, data):
        errors={}
        if len(data['message']) <= 0:
            errors["message"] = "Message should be at least 1 characters."
        return errors

class CommentValidator(models.Manager):
    def basic_validator(self, data):
        errors={}
        if len(data['comment']) <= 0:
            errors["comment"] = "Comment should be at least 1 characters."
        return errors

class  User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField()
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserValidator()

class Message(models.Model):
    user = models.ForeignKey(User, related_name ='messages')
    message_content = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name='liked_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageValidator()
    

class Comment(models.Model):
    user = models.ForeignKey(User, related_name ='comments')
    message = models.ForeignKey(Message, related_name ='comments')
    comment_content = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentValidator()
