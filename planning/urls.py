from django.urls import path
from . import views

urlpatterns = [
    path("projects/", views.proj_list, name="proj_list"),
    path("projects/<str:ref>/phases/", views.phases_per_proj, name="project_phases"),
    path(
        "projects/<str:ref>/tasks/",
        views.tasks_per_project,
        name="project_tasks",
    ),
    path(
        "projects/<str:ref>/phases/<str:phaseId>/tasks/",
        views.tasks_per_phase,
        name="phase_tasks",
    ),
]
