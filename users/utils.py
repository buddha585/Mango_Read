from datetime import datetime
import os

def path_and_rename(instance, filename):
    now = datetime.now()
    upload_to = "user_images"
    ext = filename.split(".")[-1]
    filename = f'{instance.username}{now.strftime("%d-%m-%Y")}.{ext}'
    return os.path.join(upload_to, filename)