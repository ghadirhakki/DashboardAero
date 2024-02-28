from django.contrib import admin

from core.models import FileModel, Profile, ImageModel, Alert

# Register your models here.


admin.site.register(FileModel)
admin.site.register(ImageModel)
admin.site.register(Alert)


@admin.register(Profile)
class profileAdmin(admin.ModelAdmin):
    list_display = ["user", "proj"]
