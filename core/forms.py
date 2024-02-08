from django.utils import timezone
from django import forms

from .models import FileModel


class FileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ["type", "file"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.date = timezone.now()
        if commit:
            instance.save()
        return instance
