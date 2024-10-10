import logging
import mimetypes
import os

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from portfolio.filters import MediaPositionFilter
from portfolio.models import MediaFile, MediaPosition
from portfolio.serializers import MediaFileSerializer, MediaPositionSerializer
from portfolio.task_runner import compress_media_runner

logger = logging.getLogger(__name__)


class MediaPositionViewSet(viewsets.ModelViewSet):
    queryset = MediaPosition.objects.all()
    serializer_class = MediaPositionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MediaPositionFilter
    lookup_field = 'slug'

    def get_object(self):
        # Override to find the MediaPosition by slug
        slug = self.kwargs.get('slug')
        return get_object_or_404(MediaPosition, slug=slug)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_positions = MediaPosition.objects.order_by('-created_at')[:5]
        serializer = self.get_serializer(recent_positions, many=True)
        return Response(serializer.data)


class VideoThumbnailView(APIView):
    def get(self, request, uuid):
        try:
            media_file = MediaFile.objects.get(pk=uuid)
        except MediaFile.DoesNotExist:
            return JsonResponse({"error": "Media file not found"}, status=status.HTTP_404_NOT_FOUND)

        if media_file.file_type != 'video':
            return JsonResponse({"error": "This media file is not a video"}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f"thumbnail_{uuid}"
        thumbnail_path = cache.get(cache_key)

        if not thumbnail_path:
            thumbnail_path = media_file.create_thumbnail()
            if not thumbnail_path:
                return JsonResponse({"error": "Thumbnail creation failed"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            cache.set(cache_key, thumbnail_path, timeout=settings.REDIS_CACHE_TIMEOUT)

        return HttpResponseRedirect(thumbnail_path)


class MediaFileListView(generics.ListAPIView):
    queryset = MediaFile.objects.filter(is_public=True)
    serializer_class = MediaFileSerializer


class MediaFileView(APIView):
    def get(self, request, uuid, *args, **kwargs):
        try:
            media_file = MediaFile.objects.prefetch_related('processedmediafile_set').get(pk=uuid)
        except MediaFile.DoesNotExist:
            logger.error(f"Media file with UUID {uuid} not found.")
            return JsonResponse({"error": "Media file not found"}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated and not media_file.is_public:
            return JsonResponse({"error": "This media file is not public"}, status=status.HTTP_403_FORBIDDEN)

        resolution = request.GET.get('resolution')
        quality = request.GET.get('quality')

        if resolution:
            try:
                width, height = map(int, resolution.split(','))
                resolution = (width, height)
            except ValueError:
                return JsonResponse({"error": "Invalid resolution format. Use width,height"},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            resolution = None

        if quality:
            try:
                quality = int(quality)
                if not (1 <= quality <= 100):
                    raise ValueError
            except ValueError:
                return JsonResponse({"error": "Quality must be an integer between 1 and 100"},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            quality = 75

        cache_key = f"media_{uuid}_res_{resolution}_qual_{quality}"
        cached_file = cache.get(cache_key)
        # if cached_file:
        #     logger.info(f"Serving cached file for UUID {uuid} with resolution {resolution} and quality {quality}")
        #     return FileResponse(open(cached_file['content'], 'rb'), content_type=cached_file['content_type'])

        processed_file = media_file.processedmediafile_set.filter(resolution=resolution, quality=quality).first()
        content_type = 'video/mp4' if media_file.file_type == 'video' else 'image/jpeg'
        if not processed_file or processed_file.status != 'processed':
            logger.info(f"File not processed yet for UUID {uuid}. Starting compression.")
            try:
                compress_media_runner(media_file.pk, resolution, quality)
            except Exception as e:
                logger.error(f"An error occurred while fetching processed file for UUID {uuid}: {e}")
                return JsonResponse({"error": "An error occurred while fetching processed file"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return FileResponse(open(media_file.file.path, 'rb'), content_type=content_type)

        logger.info(f"Serving processed file for UUID {uuid} from path: {processed_file.processed_file.name}")

        if os.path.exists(processed_file.processed_file.name):
            cache.set(cache_key, {'content': processed_file.processed_file.name, 'content_type': content_type},
                      timeout=settings.REDIS_CACHE_TIMEOUT)
            return FileResponse(open(processed_file.processed_file.name, 'rb'), content_type=content_type)
        else:
            logger.error(f"Processed file not found for UUID {uuid} at path {processed_file.processed_file.name}")
            return JsonResponse({"error": "Processed file not found"}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def upload_media(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        file_urls = []

        for file in files:
            try:
                mime_type, _ = mimetypes.guess_type(file.name)
                file_type = None
                if mime_type:
                    if mime_type.startswith('image'):
                        file_type = 'image'
                    elif mime_type.startswith('video'):
                        file_type = 'video'

                media_file = MediaFile(
                    file_type=file_type,
                    title=file.name
                )
                media_file.file = file
                media_file.save()

                file_urls.append(media_file)
            except Exception as e:
                return JsonResponse({'error': f'Error processing file: {file.name}, {str(e)}'}, status=500)

        return JsonResponse(MediaFileSerializer(file_urls, many=True).data, safe=False, status=201)
