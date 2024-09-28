from django.shortcuts import render, redirect

from backend.portfolio.forms import MediaFileForm
from backend.portfolio.models import MediaFile


def upload_media(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('media_list')
    else:
        form = MediaFileForm()
    return render(request, 'portfolio/upload_media.html', {'form': form})

def media_list(request):
    media_files = MediaFile.objects.all()
    return render(request, 'portfolio/media_list.html', {'media_files': media_files})