from datetime import datetime

def log_upload(filename):
    with open("/logs/uploads.log", "a") as f:
        f.write(f"{datetime.now().isoformat()} - UPLOADED: {filename}\n")

def log_metadata(caption, face_info):
    with open("/logs/analysis.log", "a") as f:
        f.write(f"{datetime.now().isoformat()} - METADATA: {caption}, {face_info}\n")
