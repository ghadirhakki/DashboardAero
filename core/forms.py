import csv
from django.utils import timezone
from django import forms

from .models import FileModel, ImageModel


class FileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ["type", "file", "project_ref"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.date = timezone.now()
        if commit:
            instance.save()
        return instance


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ["img", "project_ref"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.date = timezone.now()
        if commit:
            instance.save()
        return instance
