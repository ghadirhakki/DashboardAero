from django.db import models
from rest_framework import serializers


# Create your models here.
class ProjectModel(models.Model):
    reference = models.CharField(max_length=20)  ## should be format : MA_0321/09
    name = models.CharField(max_length=80, blank=True)
    start = models.DateField()
    end = models.DateField()


class ProjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = "__all__"


class PhaseModel(models.Model):
    project_related = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    start = models.DateField()
    end = models.DateField()


class PhaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhaseModel
        fields = "__all__"


class TaskModel(models.Model):  # Name,Duration,Start,Finish
    project_related = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    phase_related = models.ForeignKey(PhaseModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    start = models.DateField()
    end = models.DateField()


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = "__all__"
