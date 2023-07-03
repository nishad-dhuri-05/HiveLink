from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room , Topic, Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm
from django.contrib import messages

# Create your views here.

# rooms=[
#     {'id':1,'name':'Python'},
#     {'id':2,'name':'Javascript'},
#     {'id':3,'name':'C++'},
# ]

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    

    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objectss.get(username=username)
        except:
            messages.error(request,'User does not exist')
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)#also adds the session
            return redirect('home')
        else:
            messages.error(request,'Username or password is incorrect')

    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page='register'
    form =UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)#commit =false in order ot get the user object directly
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')
    context={'page':page,'form':form}
    return render(request,'base/login_register.html',context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''

    #rooms=Room.objects.filter(topic__name__icontains=q) #.objects is a model manager
    # the i in icontains is to not make it case sensitive
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    room_count=rooms.count()
    topics=Topic.objects.all()
    room_messages=Message.objects.filter(
        Q(room__name__icontains=q)|
        Q(room__topic__name__icontains=q)
    )
    #.get() .filter .exclude are the other methods
    #return HttpResponse('Home Page')
    #return render(request,'home.html',{'rooms':rooms})
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()#.order_by('-created')#put the name of the model in small case
    participants=room.participants.all()#for many to many no need to use _set 
    # rooms=Room.objects.all()
    # for i in rooms:
    #     if i.id==int(pk):
    #         room=i 
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    context={'room':room,'room_messages':room_messages,'participants':participants}
    #return HttpResponse('Room')
    return render(request,'base/room.html',context)


def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)



@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        print(request.POST)
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')#enter the 'name'

    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user!=room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)#specify which room needs to be updated
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context={'form':form,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)

    if request.user!=room.host:
        return HttpResponse('You are not allowed to perform this action!!')
    
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)

    if request.user!=message.user:
        return HttpResponse('You are not allowed to perform this action!!')
    
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})