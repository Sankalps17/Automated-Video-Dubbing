from django import forms
from .models import VideoFile

LANGUAGE_CHOICES = [
    ('kn', 'Kannada'),
    ('te', 'Telugu'),
    ('ta', 'Tamil'),
    ('hi', 'Hindi'),
]

class VideoUploadForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, label="Select Language")
    
    class Meta:
        model = VideoFile
        fields = ['original_video', 'language']
