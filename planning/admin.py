from django.contrib import admin

from .models import ProjectModel, PhaseModel, TaskModel

# Register your models here.


@admin.register(ProjectModel)
class projmodelAdmin(admin.ModelAdmin):
    list_display = ["reference", "name"]


admin.site.register(PhaseModel)
admin.site.register(TaskModel)
