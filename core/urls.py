from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("fileupload", views.upload_file, name="file_upload"),
]
