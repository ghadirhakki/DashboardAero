from django.db import models

FILE_CHOICES = (("BudgetFile", "Budget File"), ("PlanningFile", "Planning File"))


# Create your models here.
class FileModel(models.Model):
    type = models.CharField(max_length=20, choices=FILE_CHOICES)
    file = models.FileField(upload_to="files/")
    date = models.DateTimeField()
    project_ref = models.CharField(max_length=20, blank=True)
