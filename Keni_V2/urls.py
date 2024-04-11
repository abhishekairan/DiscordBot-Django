"""Keni_V2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website.views import *
from website import dcGate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main,name='default'),
    path('home/',main,name='default'),
    path('login/',Discordlogin,name='login'),
    path('logout/',discordLogout,name='logout'),
    path('auth/',authenticateUser,name='loggedin'),
    path('embed/',dcGate.embed,name='embed'),
    path('ticket/',dcGate.ticket,name='ticket'),
    path('guild/<int:id>',guild,name="guild"),
    path('guild/message/<int:id>',guild_message,name="guild_message"),
    path('delete/message/<int:channelid>/<int:messageid>/<int:guildid>',deleteMessage,name="delete_message"),
    path('guild/channels/<int:id>',guild_channels,name="guild_message"),
]
