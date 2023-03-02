from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse


class CreatePerfil(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('CreatePerfil')


class UpdatePerfil(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('UpdatePerfil')


class LoginPerfil(UpdatePerfil):
    def get(self, request, *args, **kwargs):
        return HttpResponse('LoginPerfil')


class LogoutPerfil(LoginPerfil):
    def get(self, request, *args, **kwargs):
        return HttpResponse('LogoutPerfil')
