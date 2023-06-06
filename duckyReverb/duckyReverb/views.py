"""
Copyright (c) 2023 NewPolygons.

This file is part of DuckyReverb.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""




from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from . import functions
import os
import shutil


def home(request):
    return render(request, 'duckyReverb/newindex.html')

# New
def app(request):
    if request.method == "POST":
        link = request.POST['link']
        print(link)
        info = functions.parseLink(link)
        songDir = info[2]
        songImage = info[3][0]
        songName = info[3][1]
        colors = info[4]

        filePath = "media/" + songDir + "/stretched.wav"
        context = {'song' : filePath , 'image' : songImage, 'name' : songName ,'download' : songDir, 'colors': colors}
        print(context)
        return render(request, 'duckyReverb/appdownload.html', context={"mydata" : context})
    
    return render(request, 'duckyReverb/app.html')



def about(request):
    return render(request, 'duckyReverb/about.html')

def tutorial(request):
    return render(request, 'duckyReverb/tutorial.html')
    
def handle_not_found(request, exception):
    return render(request, 'duckyReverb/404.html')

def handle_server_error(request):
    return render(request, 'duckyReverb/500.html')
       
def apps(request, link):

    speed = link[-1]
    link = link[:-1]

    print(speed)
    print(link)
    info = functions.parseLink(link, speed)
    songDir = info[2]
    songName = info[3][1]
    #create zip archive for sending
    shutil.make_archive(settings.MEDIA_ROOT + '/' + songDir, 'zip', settings.MEDIA_ROOT + '/' +  songDir)

    #clean up old folder since we arnt using it for web
    shutil.rmtree(settings.MEDIA_ROOT + '/' + songDir)


    #send file out
    filePath = os.path.join(settings.MEDIA_ROOT, songDir + '.zip')
    if os.path.exists(filePath):
        with open(filePath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/x-zip-compressed")
            response['Content-Disposition'] = 'inline; filename=' + songName + ".zip"
            
            return response
    
        raise Http404





def appDownload(request, link):
    filePath = os.path.join