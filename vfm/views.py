# -*- coding: utf-8 -*-

import os
import shutil
import tempfile, zipfile
import time, datetime

from django.core.servers.basehttp import FileWrapper

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str

def pathGuard(request_path, base_path):
    compare = os.path.commonprefix([ os.path.abspath(request_path), base_path ])
    if compare == base_path:
        return True

def fallowPath(directory):
    files_array = []
    list_dir = []
    mime2exts_list = [

    ["application-msword", "doc", "glyphicon-file"],
    ["application-x-ms-dos-executable", "exe", "glyphicon-cog"],
    ["application-x-ms-dos-executable", "msi", "glyphicon-cog"],
    ["application-ogg", "ogg", "glyphicon-music"],
    ["application-pdf", "pdf", "glyphicon-file"],
    ["application-postscript" ,"ps", "glyphicon-file"],
    ["application-rdf+xml" , "rdf", "glyphicon-file"],
    ["application-zip", "air", "glyphicon-compressed"],
    ["application-vnd.ms-excel" ,"xls", "glyphicon-file"],
    ["application-vnd.ms-powerpoint","ppt", "glyphicon-file"],
    ["application-vnd.rn-realmedia","rm", "glyphicon-file"],
    ["application-x-dvi", "dvi", "glyphicon-film"],
    ["application-x-javascript", "js", "glyphicon-file"],
    ["text-x-script", "sh", "glyphicon-file"],
    ["application-x-shockwave-flash", "swf", "glyphicon-film"],
    ["application-zip", "tar", "glyphicon-compressed"],
    ["audio-x-wav", "wav", "glyphicon-music"],
    ["image-x-generic", "jpg", "glyphicon-picture"],
    ["image-x-generic", "jpeg", "glyphicon-picture"],
    ["image-x-generic", "png", "glyphicon-picture"],
    ["image-svg+xml", "svg", "glyphicon-picture"],
    ["image-x-generic", "ico", "glyphicon-picture"],
    ["text-css", "css", "glyphicon-file"],
    ["text-html", "html", "glyphicon-file"],
    ["text-html", "htm", "glyphicon-file"],
    ["text-html", "xhtml", "glyphicon-file"],
    ["text-plain", "txt", "glyphicon-file"],
    ["text-rtf", "rtf", "glyphicon-file"],
    ["text-sgml", "sgml", "sgm",  "glyphicon-file"],
    ["video-x-generic", "mpg", "glyphicon-film"],
    ["video-x-generic", "mpeg", "glyphicon-film"],
    ["video-x-generic", "mpe", "glyphicon-film"],
    ["video-x-generic", "mov", "glyphicon-film"],
    ["video-x-generic", "qt", "glyphicon-film"],
    ["video-x-generic", "m4u", "glyphicon-film"],
    ["video-x-generic", "flv", "glyphicon-film"],
    ["video-x-generic", "avi", "glyphicon-film"],
    ["video-x-generic", "movie", "glyphicon-film"]]

    list = sorted(os.listdir(directory))

    for item in list:
        if not item.startswith('.'):
            path = os.path.join(directory, item)
            rpath = os.path.relpath(path, settings.COMMANDER_ROOT_DIR)
            m_time = datetime.datetime.strptime(time.ctime(os.stat(path).st_mtime), "%a %b %d %H:%M:%S %Y")
            a_time = datetime.datetime.strptime(time.ctime(os.stat(path).st_atime), "%a %b %d %H:%M:%S %Y")
            size = os.stat(path).st_size

            if os.path.isdir(path):
                files_array.append({"type":0,
                                    "fname":item,
                                    "rpath":rpath,
                                    "mtime":m_time,
                                    "atime":a_time,
                                    "size":size,
                                    "mime":"",
                                    "ico":"glyphicon-folder-close"})

            elif os.path.isfile(path):
                mime = "unknown"
                ico = "glyphicon-file"
                ext = item.split(".")[-1].strip().lower()

                for e in mime2exts_list:

                    if e[1] == ext:
                        mime = e[0]
                        ico = e[2]

                files_array.append({"type":1,
                                    "fname":item,
                                    "rpath":rpath,
                                    "mtime":m_time,
                                    "atime":a_time,
                                    "fsize":size,
                                    "fmime":mime,
                                    "ico": ico})

        list_dir = sorted(files_array, key=lambda file: str(file["type"]))

    return list_dir


def handleUploadedFile(f,name, path):
    with open('{}/{}/{}'.format(settings.COMMANDER_ROOT_DIR, path, name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required
def uploadFile(request):
    username = request.user.username
    home = "{}{}".format(settings.COMMANDER_ROOT_DIR, username)
    data = {}
    if request.method == 'POST':
        if request.POST['fname'] and request.POST['fpath']:
            abspath = "{}{}".format(settings.COMMANDER_ROOT_DIR, request.POST['fpath'])
            guard_request = pathGuard(abspath, home)
            if guard_request == True:
                handleUploadedFile(request.FILES['fdata'],request.POST['fname'],request.POST['fpath'])
                success = True
                msg = u" <b>\"{}\" has uploaded succesfuly</b>".format(request.POST['fname'])

            data = {"success":success,
                    "message":msg }
    return JsonResponse(data)

@login_required
def createDirectory(request):
    username = request.user.username
    home = "{}{}".format(settings.COMMANDER_ROOT_DIR, username)
    data = {}
    if request.method == 'POST':
        if request.POST['path'] and request.POST['dirname']:
            directory = "{}/{}".format(request.POST['path'], request.POST['dirname'])
            abspath = "{}/{}".format(settings.COMMANDER_ROOT_DIR, directory)
            guard_request = pathGuard(abspath, home)
            if guard_request == True:
                if not os.path.exists(abspath):
                    os.makedirs(abspath)
                    success = True
                    msg = u"New folder successful created <b>\"{}\"</b>".format(request.POST['dirname'])
                else:
                    success = False
                    msg = u"Folder already exist <b>\"{}\"</b>".format(request.POST['dirname'])
            else:
                success = False
                msg = u"Access denied"

            data = {"success":success,
                    "message":msg }

    return JsonResponse(data)

@login_required
def rename(request):
    username = request.user.username
    home = "{}{}".format(settings.COMMANDER_ROOT_DIR, username)
    data = {}
    if request.method == 'POST':
        if request.POST['path'] and request.POST['current'] and request.POST['rename']:
            current = "{}/{}".format(request.POST['path'], request.POST['current'])
            rename = "{}/{}".format(request.POST['path'], request.POST['rename'])
            abs_current="{}/{}".format(settings.COMMANDER_ROOT_DIR, current)
            abs_rename = "{}/{}".format(settings.COMMANDER_ROOT_DIR, rename)
            guard_request_current = pathGuard(abs_current, home)
            guard_request_rename = pathGuard(abs_rename, home)
            if guard_request_current == True and guard_request_rename == True:
                if os.path.exists(abs_current) and not os.path.exists(abs_rename):
                    os.rename(abs_current, abs_rename)
                    success = True
                    msg = u"<b>\"{}\"</b> successful renamed to <b>\"{}\"</b>".format(request.POST['current'], request.POST['rename'])
                else:
                    success = False
                    msg = u"Folder already exist <b>\"{}\"</b>".format(request.POST['rename'])
            else:
                success = False
                msg = u"Access denied"

            data = {"success":success,
                    "message":msg }

    return JsonResponse(data)

@login_required
def moveToTrash(request):
    username = request.user.username
    home = "{}{}".format(settings.COMMANDER_ROOT_DIR, username)
    trash = "{}/.Trash".format(home)
    data = {}
    if request.method == 'POST':
        if request.POST['path'] and request.POST['target']:
            target = "{}/{}".format(request.POST['path'],request.POST['target'])
            abs_target = "{}/{}".format(settings.COMMANDER_ROOT_DIR, target)
            abs_destination = "{}/{}".format(trash, request.POST['target'])
            guard_request = pathGuard(abs_target,home)
            if guard_request == True:
                os.rename(abs_target, abs_destination)
                success = True
                msg = u"removed successfuly"
            else:
                success = False
                msg = u"Access denied"
            
            data = {"success":success,
                    "message":msg }
    return JsonResponse(data)

@login_required
def recovery(request):
    username = request.user.username
    home = "{}{}".format(settings.COMMANDER_ROOT_DIR, username)
    trash = "{}/.Trash".format(home)
    data = {}
    if request.method == 'POST':
        if request.POST['path'] and request.POST['target']:
            target = "{}/{}".format(request.POST['path'],request.POST['target'])
            abs_target = "{}/{}".format(settings.COMMANDER_ROOT_DIR, target)
            abs_destination = "{}/{}".format(home, request.POST['target'])
            guard_request = pathGuard(abs_target,trash)
            if guard_request == True:
                os.rename(abs_target, abs_destination)
                success = True
                msg = u"recovered successfuly"
            else:
                success = False
                msg = u"Access denied"
            
            data = {"success":success,
                    "message":msg }
    return JsonResponse(data)

@login_required
def delete(request):
    username = request.user.username
    home = "{}{}".format(settings.COMMANDER_ROOT_DIR, username)
    trash = "{}/.Trash".format(home)
    data = {}
    if request.method == 'POST':
        if request.POST['path'] and request.POST['target']:
            target = "{}/{}".format(request.POST['path'],request.POST['target'])
            abs_target = "{}/{}".format(settings.COMMANDER_ROOT_DIR, target)
            guard_request = pathGuard(abs_target,trash)
            if guard_request == True:
                try:
                    if os.path.isfile(abs_target):
                        os.remove(abs_target)
                    elif os.path.isdir(abs_target): 
                        shutil.rmtree(abs_target)
                    success = True
                    msg = u"location permanently removed"
                        
                except Exception as e:               
                    success = False
                    msg = u"<b>sys err<b/>:\" {}\"".format(e)
            else:
                success = False
                msg = u"Access denied"
            
            data = {"success":success,
                    "message":msg }
    return JsonResponse(data)
    
@login_required
def cleanTrash(request):
    username = request.user.username
    trash = "{}/{}/.Trash".format(settings.COMMANDER_ROOT_DIR, username)
    data = {}
    if request.method == 'POST':
        messages = []
        for fname in os.listdir(trash):
            target = os.path.abspath(os.path.join(trash, fname))
            try:
                if os.path.isfile(target):
                    os.remove(target)
                elif os.path.isdir(target): 
                    shutil.rmtree(target)       
            except Exception as e:               
                err = u"<b>sys err<b/>:\" {}\"".format(e)
                messages.append({"fname":fname,
                                 "msg":err})

        if messages.__len__() > 0:
            data = {"success":False,
                    "message":messages }
        else:
            data = {"success":True,
                    "message":"Trash is empty" }                         

    return JsonResponse(data) 

@login_required
def trashCounter(request):
    username = request.user.username
    trash = "{}/{}/.Trash".format(settings.COMMANDER_ROOT_DIR, username)
    if request.method == 'POST':
        counter = len(os.listdir(trash))
                     
    return JsonResponse({"files":counter})

def getDownload(request):
    username = request.user.username
    home = "{}{}".format(settings.COMMANDER_ROOT_DIR, username)
    if request.GET['path']:
        abs_path = "{}{}".format(settings.COMMANDER_ROOT_DIR, request.GET['path'])
        guard_request = pathGuard(abs_path, home)
        if guard_request == True:
            if os.path.isfile(abs_path):
                filename = abs_path                               
                wrapper = FileWrapper(file(filename))
                response = HttpResponse(wrapper, content_type='application/force-download')
                response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(abs_path)
                response['Content-Length'] = os.path.getsize(filename)
            else:
                tmp_dir = "{}/{}/.Trash".format(settings.COMMANDER_ROOT_DIR, username)
                temp = tempfile.NamedTemporaryFile(dir=tmp_dir, delete=True)                
                archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
                for foldername, subfolders, filenames in os.walk(abs_path):
                    if foldername == abs_path:
                         rel_folder_name = ''
                    else:
                        rel_folder_name = os.path.relpath(foldername, abs_path)
                    archive.write(foldername, arcname=rel_folder_name)

                    for filename in filenames:
                        archive.write(os.path.join(foldername, filename), os.path.join(rel_folder_name, filename))

                archive.close()

                wrapper = FileWrapper(file(temp.name))
                response = HttpResponse(wrapper, content_type='application/force-download')
                response['Content-Disposition'] = 'attachment; filename=%s.zip' % smart_str(request.GET['path'])
                response['Content-Length'] = os.path.getsize(temp.name)
    return response            
            

def initUserSpace(home, trash):
    if not os.path.exists(home) or not os.path.isdir(home):
        os.mkdir(os.path.join(home))

    if not os.path.exists(trash) or not os.path.isdir(trash):
        os.mkdir(os.path.join(trash))
    return True

@login_required
def commander(request):
    username = request.user.username
    home = "{}{}".format(settings.COMMANDER_ROOT_DIR, username)
    trash = "{}/.Trash".format(home)
    path = home
    relative_path = "{}/".format(username)
    errors = success = info = ""

    init_user = initUserSpace(home,trash)
    if not init_user == True:
        errors = "Cannot create user space. Please contact your administrator."
        return render(request,'index.html',{"errors":errors})
                                        
    breadcrumb = []
    if 'path' in request.GET and request.GET['path']:
        request_path = settings.COMMANDER_ROOT_DIR + request.GET['path']
        guard_request = pathGuard(request_path, home)

        if guard_request == True:
            path = request_path
            relative_path = request.GET['path']
            bread = relative_path.split('/')

            if bread.__len__() > 3:
                breadcrumb.append(["...",""])
                for crumb in bread[-2:]:
                    breadcrumb.append([crumb, "/".join(bread[:-1])])
            else:
                for crumb in bread[1:]:
                    breadcrumb.append([crumb, "/".join(bread[:-1])])
        else:
            errors = "Access denied"

    list_dir = fallowPath(path)

    return render(request,'commander.html',{'list_dir':list_dir,
                                        'path':relative_path,
                                        'breadcrumb':breadcrumb,
                                        'errors': errors,
                                        'success':success,
                                        'info':info})

@login_required
def trashFolderView(request):
    username = request.user.username
    home = "{}{}".format(settings.COMMANDER_ROOT_DIR, username)
    trash = "{}/.Trash".format(home)
    path = trash
    relative_path = "{}/.Trash".format(username)
    errors = success = info = ""

    init_user = initUserSpace(home,trash)
    if not init_user == True:
        errors = "Cannot create user space. Please contact your administrator."
        return render(request,'index.html',{"errors":errors})
                                        
    breadcrumb = []
    if 'path' in request.GET and request.GET['path']:
        request_path = settings.COMMANDER_ROOT_DIR + request.GET['path']
        guard_request = pathGuard(request_path, home)

        if guard_request == True:
            path = request_path
            relative_path = request.GET['path']
            bread = relative_path.split('/')

            if bread.__len__() > 4:
                breadcrumb.append(["...",""])
                for crumb in bread[-2:]:
                    breadcrumb.append([crumb, "/".join(bread[:-2])])
            else:
                for crumb in bread[2:]:
                    breadcrumb.append([crumb, "/".join(bread[:-2])])
        else:
            errors = "Access denied"

    list_dir = fallowPath(path)

    return render(request,'trash.html',{'list_dir':list_dir,
                                        'path':relative_path,
                                        'breadcrumb':breadcrumb,
                                        'errors': errors,
                                        'success':success,
                                        'info':info})
    