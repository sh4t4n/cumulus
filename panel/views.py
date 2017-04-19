# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.messages import error

from django.contrib.auth.models import User
from panel.forms import CreateUserForm, UpdateUserForm


@user_passes_test(lambda u:u.is_staff, login_url=None)
def createUser(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form = form.save(commit = False)
            form.password = make_password(request.POST['password'])
            form.status = 1
            form.save()
        else:
            error(request, 'Errors with internal validation')
            print form.errors
    
    return HttpResponseRedirect("/panel/users")

@user_passes_test(lambda u:u.is_staff, login_url=None)
def users(request):
    users = User.objects.all()
    return render(request, "panel/users.html", {'users':users})

@user_passes_test(lambda u:u.is_staff, login_url=None)
def checkUser(request):
    data = {}
    if request.method == 'POST':
        if request.POST['username']:
            user = User.objects.filter(username=request.POST['username'])
            if user:
                success = False
            else:
                success = True                
                
            data = { "success": success }
    return JsonResponse(data)
            
@user_passes_test(lambda u:u.is_staff, login_url=None)
def deleteUser(request):
    data = {}
    if request.method == 'POST':
        if request.POST['user_id']:
            try:
                user= User.objects.get(pk=request.POST['user_id'])
            except User.DoesNotExist:
                user = None
            if user and not user.is_superuser:
                user.delete()
                success = True
            else:
                success = False
                
            data = { "success": success }
    return JsonResponse(data)
    
@user_passes_test(lambda u:u.is_staff, login_url="/")
def editUser(request):
    data = {}
    success = False
    details = ""
    if request.method == 'POST':
        if 'user_id' in request.POST and request.POST['user_id']:
            try:
                instance = User.objects.get(pk=request.POST['user_id'])
            except User.DoesNotExist:
                instance = None
            if instance:    
                form = UpdateUserForm(request.POST or None, instance=instance)
                if form.is_valid():
                    form.save()
                    success = True
                    msg = "User was updated successfully"
                else:
                    msg = "Validation error"
                    details = form.errors
            else:
                msg = "User does no exist"
        else:
            msg = "Bad request"
        
        data = { "success": success,"messages":msg, "details":details }
    return JsonResponse(data)