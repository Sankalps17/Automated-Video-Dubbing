import json
import os
from django.conf import settings

PROGRESS_FILE = os.path.join(settings.MEDIA_ROOT, 'progress.json')

def update_progress(task, progress):
    data = {}
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as file:
            data = json.load(file)
    
    data[task] = progress
    with open(PROGRESS_FILE, 'w') as file:
        json.dump(data, file)
