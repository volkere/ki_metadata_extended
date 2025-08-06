from datetime import datetime
import json
import os

def ensure_log_directory():
    """Ensure the logs directory exists"""
    os.makedirs("/logs", exist_ok=True)

def log_upload(filename):
    ensure_log_directory()
    try:
        with open("/logs/uploads.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - UPLOADED: {filename}\n")
    except Exception as e:
        print(f"Error logging upload: {e}")

def log_metadata(caption, face_info):
    ensure_log_directory()
    try:
        # Convert data to JSON for better serialization
        log_data = {
            "caption": caption,
            "face_info": face_info
        }
        
        with open("/logs/analysis.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - METADATA: {json.dumps(log_data, ensure_ascii=False)}\n")
    except Exception as e:
        print(f"Error logging metadata: {e}")
        # Fallback to string representation
        try:
            with open("/logs/analysis.log", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().isoformat()} - METADATA: {str(caption)}, {str(face_info)}\n")
        except Exception as e2:
            print(f"Fallback logging also failed: {e2}")

def log_error(error_message, details=None):
    ensure_log_directory()
    try:
        error_data = {
            "error": error_message,
            "details": details
        }
        
        with open("/logs/errors.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - ERROR: {json.dumps(error_data, ensure_ascii=False)}\n")
    except Exception as e:
        print(f"Error logging error: {e}")
