from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("file_upload/", views.upload_file, name="file_upload"),
    path("dir_dashboard/", views.dir_dashboard, name="dir_dashboard"),
    path("proj_list/", views.proj_list, name="proj_list"),
    path("proj_phase_list/<str:ref>/", views.phases_per_proj, name="phase_proj"),
    path("proj_tasks_list/<str:ref>/", views.tasks_per_phase, name="tasks_proj"),
    path(
        "financial_records_per_proj/<str:ref>/",
        views.financial_records_per_proj,
        name="financial_records_per_proj",
    ),
    path(
        "financial_records_list/",
        views.financial_records_list,
        name="financial_records_list",
    ),
    # path("pmdashboard", views.pm_dashboard, name="pm_dashboard"),
    # path("techdashboard", views.tech_dashboard, name="tech_dashboard"),
]
