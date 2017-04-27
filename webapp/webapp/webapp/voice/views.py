from django.http import HttpResponseRedirect
from django.shortcuts import render

from webapp.voice.models import FileModel
from .forms import UploadFileForm


# Imaginary function to handle an uploaded file.


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = FileModel(file=request.FILES['file'])
            instance.save()
            return HttpResponseRedirect('/success/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def success(request):
    return render(request, 'success.html')
