from django.db import models

class VideoFile(models.Model):
    original_video = models.FileField(upload_to='original_videos/')
    extracted_audio = models.CharField(max_length=200, blank=True)
    transcription = models.CharField(max_length=200, blank=True)
    translated_audio = models.CharField(max_length=200, blank=True)
    dubbed_video = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video uploaded at {self.uploaded_at}"