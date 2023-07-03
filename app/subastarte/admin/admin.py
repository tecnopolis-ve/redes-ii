from django.urls import reverse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u:u.is_superuser)
def index(request):
    return render(request, "admin/admin/index.html")