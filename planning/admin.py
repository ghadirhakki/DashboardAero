from django.contrib import admin

from .models import ProjectModel, PhaseModel, TaskModel

# Register your models here.


admin.site.register(ProjectModel)
admin.site.register(PhaseModel)
admin.site.register(TaskModel)
