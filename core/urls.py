from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("file_upload/", views.upload_file, name="file_upload"),
    path("dir_dashboard/", views.dir_dashboard, name="dir_dashboard"),
    # path("pmdashboard", views.pm_dashboard, name="pm_dashboard"),
    # path("techdashboard", views.tech_dashboard, name="tech_dashboard"),
]
