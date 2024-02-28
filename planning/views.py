from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import (
    ProjectModel,
    ProjectModelSerializer,
    PhaseModel,
    PhaseModelSerializer,
    TaskModel,
    TaskModelSerializer,
)

from rest_framework.response import Response


# Create your views here.


@api_view()
def proj_list(request):
    if request.method == "GET":
        all_projects = ProjectModel.objects.all()
        serializer = ProjectModelSerializer(all_projects, many=True)
        return Response(serializer.data)


@api_view()
def phases_per_proj(request, ref):
    if request.method == "GET":
        project_phases = PhaseModel.objects.filter(project_related__reference=ref)
        serializer = PhaseModelSerializer(project_phases, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def tasks_per_project(request, ref):
    project_phases = PhaseModel.objects.filter(project_related__reference=ref)
    phase_tasks = TaskModel.objects.filter(project_related__reference=ref)
    data = {"phases": project_phases, "tasks": phase_tasks}
    return Response(data)


@api_view(["GET"])
def tasks_per_phase(request, ref, phaseId):
    phase_tasks = TaskModel.objects.filter(
        project_related__reference=ref, phase_related=phaseId
    )
    serializer = TaskModelSerializer(phase_tasks, many=True)
    return Response(serializer.data)
