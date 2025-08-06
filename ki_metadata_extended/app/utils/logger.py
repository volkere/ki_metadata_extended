from datetime import datetime
import json
import os
import numpy as np

def ensure_log_directory():
    """Ensure the logs directory exists"""
    os.makedirs("/logs", exist_ok=True)

def convert_to_json_serializable(obj):
    """Convert objects to JSON serializable format"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    else:
        return obj

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
        # Convert data to JSON serializable format
        log_data = {
            "caption": caption,
            "face_info": convert_to_json_serializable(face_info)
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
            "details": convert_to_json_serializable(details) if details else None
        }
        
        with open("/logs/errors.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - ERROR: {json.dumps(error_data, ensure_ascii=False)}\n")
    except Exception as e:
        print(f"Error logging error: {e}")
