from django import forms

from webapp.voice.models import FileModel


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ['file']
