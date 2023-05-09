from datetime import datetime
import os

def path_and_rename_cover(instance, filename):
    now = datetime.now()
    upload_to = "manga_covers"
    ext = filename.split(".")[-1]
    filename = f"{instance.manga_name}{now.strftime('%d-%m-%Y %H-%M')}.{ext}"
    return os.path.join(upload_to, filename)