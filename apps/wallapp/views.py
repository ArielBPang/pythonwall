from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                birthday=request.POST['birthday'],
                email=request.POST['email'],
                password=pw_hash
            )
            request.session['user_id'] = new_user.id
            request.session['first_name'] = new_user.first_name
            request.session['email'] = new_user.email
            return render(request, 'welcome.html')


def welcome(request):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in!")
        return redirect ('/')
    context ={
        # i used to have users here but i can pull user info in html with commands
        'posts': Message.objects.all()
    }
    return render(request,'wall.html', context)


def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
        except:
            messages.error(
                request, "Either your email or password was input incorrectly.")
            return redirect('/')
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()): 
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            return redirect('/welcome')
        else:
            messages.error(
                request, "Either your email or password was input incorrectly.")
            return redirect('/')

    
def logout(request):
    request.session.clear()
    return redirect('/')

def message(request):
    errors = Message.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/welcome')
    else:
        Message.objects.create(user=User.objects.get(id=request.session['user_id']), message_content=request.POST['message'])
    return redirect('/welcome')

def comment(request):
    errors = Comment.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/welcome')
    else:
        Comment.objects.create(user=User.objects.get(id=request.session['user_id']), message=Message.objects.get(id=request.POST['message_id']), comment_content=request.POST['comment'])
    return redirect('/welcome')
    # parent message named in HTML 

def messagelike(request, message_id):
    message=Message.objects.get(id=message_id)
    # print(message.message_content)
    user=User.objects.get(id=request.session['user_id'])
    # print(user.first_name)
    # message.likes.add(user)
    user.liked_messages.add(message)
    user.save()
    # what i named it in models (likes)
    return redirect('/welcome')

def messageunlike(request, message_id):
    message=Message.objects.get(id=message_id)
    user=User.objects.get(id=request.session['user_id'])
    user.liked_messages.remove(message)
    user.save()
    return redirect('/welcome')

    # unlike is similar but with user.likedmessage.remove

def commentlike(request, comment_id):
    comment=Comment.objects.get(id=comment_id)
    user=User.objects.get(id=request.session['user_id'])
    user.liked_comments.add(comment)
    user.save()
    return redirect('/welcome')

def commentunlike(request, comment_id):
    comment=Comment.objects.get(id=comment_id)
    user=User.objects.get(id=request.session['user_id'])
    user.liked_comments.remove(comment)
    user.save()
    return redirect('/welcome')


def delete_comment(request, comment_id):
    comment=Comment.objects.get(id = comment_id)
    if not request.session['user_id'] == comment.user.id:
        messages.error(request, "Must have created to delete this post!")
        return redirect ('welcome')
    else:
        comment.delete()
    return redirect('/welcome')

def delete_message(request, message_id):
    message=Message.objects.get(id = message_id)
    if not request.session['user_id'] == message.user.id:
        messages.error(request, "Must have created to delete this post!")
        return redirect ('welcome')
    else:
        message.delete()
    return redirect('/welcome')