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


@api_view()
def tasks_per_project(request, ref):
    if request.method == "GET":
        project_phases = PhaseModel.objects.filter(project_related__reference=ref)
        phase_serializer = PhaseModelSerializer(project_phases, many=True)
        phase_tasks = TaskModel.objects.filter(project_related__reference=ref)
        task_serializer = TaskModelSerializer(phase_tasks, many=True)
        response_data = {"phases": phase_serializer.data, "tasks": task_serializer.data}
        return Response(response_data)
