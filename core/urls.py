from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("file_upload/", views.upload_file, name="file_upload"),
    path("image_upload/", views.upload_image, name="image_upload"),
    path("dir_dashboard/", views.dir_dashboard, name="dir_dashboard"),
    path("cp_dashboard/", views.cp_dashboard, name="cp_dashboard"),
    path("cp_dashboard/<str:ref>/", views.cp_dashboard, name="cp_dashboard"),
    path("tech_dashboard/", views.tech_dashboard, name="tech_dashboard"),
    path("tech_dashboard/<str:ref>/", views.tech_dashboard, name="tech_dashboard"),
    path("proj_details/<str:ref>/", views.phases_per_proj, name="phases"),
    path("chart_proj_pie/<str:ref>/", views.chart_proj_pie, name="chart_proj_pie"),
    # path("pmdashboard", views.pm_dashboard, name="pm_dashboard"),
    # path("techdashboard", views.tech_dashboard, name="tech_dashboard"),
]
