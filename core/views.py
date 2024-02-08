from django.shortcuts import render

from django.views.generic import TemplateView, CreateView

from core.forms import FileForm
from .models import FileModel

# Create your views here.


def home(request):
    return render(
        request,
        "home.html",
    )


def upload_file(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    else:
        form = FileForm()

    return render(request, "file_upload.html", {"form": form})
