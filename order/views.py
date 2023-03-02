from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

class Payment(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Payment')


class CloseOrder(Payment):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Close order')


class Detail(CloseOrder):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Detail order')

