from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path("",views.index,name='home'),
    path("submitform",views.showsummary,name='submitform'),
    path("audiosubmitform",views.audiosubmitform,name='audiosubmitform'),
    path("mictotext",views.mictotext,name='mictotext'),
    path("mictextgenerate",views.mictextgenerate,name='mictextgenerate'),
    path("videotomp3",views.videotomp3,name='videotomp3'),
    path("textgenerate",views.textgenerate,name='textgenerate'),
    path("videototext",views.videototext,name='videototext'),
    path("texttosummary",views.texttosummary,name='texttosummary'),
    path("textsummary",views.textsummary,name='textsummary')
]
