from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from portfolio.forms import MediaFileForm
from portfolio.image import process_image
from portfolio.models import MediaFile
from portfolio.serializers import MediaFileSerializer


class MediaFileListView(generics.ListAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer


class MediaFileView(APIView):
    def get(self, request, uuid, *args, **kwargs):
        media_file = get_object_or_404(MediaFile, pk=uuid)

        if not request.user.is_authenticated and not media_file.is_public:
            return Response({"error": "This media file is not public"},
                            status=status.HTTP_403_FORBIDDEN)
        resolution = request.GET.get('resolution')
        quality = request.GET.get('quality')

        if resolution:
            try:
                width, height = map(int, resolution.split(','))
                resolution = (width, height)
            except ValueError:
                return Response({"error": "Invalid resolution format. Use width,height"},
                                status=status.HTTP_400_BAD_REQUEST)

        if quality:
            try:
                quality = int(quality)
                if not (1 <= quality <= 100):
                    raise ValueError
            except ValueError:
                return Response({"error": "Quality must be an integer between 1 and 100"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            quality = 75
        if media_file.file_type == 'image':
            file = process_image(media_file.file, resolution, quality)
        else:
            file = media_file.file

        content_type = 'image/jpeg' if media_file.file_type == 'image' else 'video/mp4'
        return HttpResponse(file, content_type=content_type)


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
