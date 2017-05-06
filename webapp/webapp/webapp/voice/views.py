from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from webapp.voice.models import FileModel
from .forms import UploadFileForm
from webapp.motion.functions import classify_sample

# Imaginary function to handle an uploaded file.


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # instance = FileModel(file=request.FILES['file'])
            # instance.save()
            result = classify_sample(request.FILES['file'])
            url = reverse('success', args=(result,))
            return HttpResponseRedirect(url)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def success(request, class_name):
    return render(request, 'success.html', class_name)

