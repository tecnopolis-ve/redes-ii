from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def index(request):
    return render(request, "public/public/index.html")