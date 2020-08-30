from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'layout_generator/home.html')