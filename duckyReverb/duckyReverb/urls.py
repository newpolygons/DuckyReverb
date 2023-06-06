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




from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('app/', views.app, name='app'),
    path('about/', views.about, name='about'),
    path('tutorial', views.tutorial, name='tutorial'),
    path('zzzyyy/', admin.site.urls), 
    path('apps/<path:link>/', views.apps, name='apps')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404="duckyReverb.views.handle_not_found"
handler500="duckyReverb.views.handle_server_error"



# Could not match any of the results on YouTube for "FKJ, ((( O ))) - Ylang Ylang". Skipping