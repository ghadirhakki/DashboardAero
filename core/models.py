from django.db import models
from django.contrib.auth.models import User
from planning.models import ProjectModel

FILE_CHOICES = (("BudgetFile", "Budget File"), ("PlanningFile", "Planning File"))


# Create your models here.
class FileModel(models.Model):
    type = models.CharField(max_length=20, choices=FILE_CHOICES)
    file = models.FileField(upload_to="files/")
    date = models.DateTimeField()
    project_ref = models.CharField(max_length=20, blank=True)


class ImageModel(models.Model):
    img = models.ImageField(upload_to="images/")
    date = models.DateTimeField()
    project_ref = models.CharField(max_length=20, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add your custom fields here
    proj = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)


class Alert(models.Model):
    msg = models.CharField(max_length=100)
    proj_related = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    va = models.IntegerField(default=0)
    vp = models.IntegerField(default=0)
