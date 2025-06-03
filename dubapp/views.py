from django.shortcuts import render
from django.http import HttpResponse, FileResponse, JsonResponse
from django.core.files.storage import default_storage
from .dubbing_script import process_video
import os, json
from django.conf import settings

def video_upload(request):
    if request.method == 'POST':
        print("Form submitted")  # Debug print statement
        video_file = request.FILES.get('video')
        language = request.POST.get('language')
        print("Received video file:", video_file)  # Debug print statement
        print("Selected language:", language)  # Debug print statement
        if video_file:
            video_path = default_storage.save(video_file.name, video_file)
            output_video_path = process_video(video_path, language)  # Pass language to process_video
            output_file_name = os.path.basename(output_video_path)
            context = {
                'output_file_name': output_file_name,
                'preview_url': os.path.join(settings.MEDIA_URL, output_file_name),
            }
            return render(request, 'dubapp/video_preview.html', context)
    return render(request, 'dubapp/upload.html')


def download_video(request):
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        if file_name:
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            if os.path.exists(file_path):
                response = FileResponse(open(file_path, 'rb'))
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response
    return HttpResponse("File not found", status=404)


def progress(request):
    progress_file = os.path.join(settings.MEDIA_ROOT, 'progress.json')
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            progress_data = json.load(file)
    else:
        progress_data = {}
    
    return JsonResponse(progress_data)