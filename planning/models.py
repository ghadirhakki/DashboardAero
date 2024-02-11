from django.db import models


# Create your models here.
class ProjectModel(models.Model):
    reference = models.CharField(max_length=20)
    name = models.CharField(max_length=80, blank=True)
    start = models.DateField()
    end = models.DateField()


class PhaseModel(models.Model):
    project_related = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    start = models.DateField()
    end = models.DateField()


class TaskModel(models.Model):  # Name,Duration,Start,Finish
    project_related = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    phase_related = models.ForeignKey(PhaseModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    start = models.DateField()
    end = models.DateField()
