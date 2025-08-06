import torch
from transformers import CLIPProcessor, CLIPModel
from deepface import DeepFace
from PIL import Image
import io
import tempfile
import os
import numpy as np
from neo4j import GraphDatabase
from app.utils.logger import log_metadata

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

NEO4J_URI = "bolt://neo4j:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

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
    elif isinstance(obj, torch.Tensor):
        return obj.tolist()
    else:
        return obj

def store_metadata_to_neo4j(caption, age, gender):
    try:
        with driver.session() as session:
            session.run(
                "MERGE (d:Description {text: $caption}) "
                "MERGE (p:Person {age: $age, gender: $gender}) "
                "MERGE (d)-[:DESCRIBES]->(p)",
                caption=caption, age=age, gender=gender
            )
    except Exception as e:
        print(f"Neo4j error: {e}")

def process_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # CLIP analysis
        inputs = clip_processor(text=["a photo", "a person", "a performance"], images=image, return_tensors="pt", padding=True)
        outputs = clip_model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1).tolist()[0]
        labels = ["a photo", "a person", "a performance"]
        caption = labels[probs.index(max(probs))]

        # DeepFace analysis - save image to temp file first
        face_info = {"error": "No face detected"}
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                image.save(tmp_file.name, 'JPEG')
                face_result = DeepFace.analyze(img_path=tmp_file.name, actions=['age', 'gender'], enforce_detection=False)
                face_info = face_result[0] if isinstance(face_result, list) else face_result
                os.unlink(tmp_file.name)  # Clean up temp file
        except Exception as e:
            face_info = {"error": str(e)}

        # Convert face_info to JSON serializable format
        face_info = convert_to_json_serializable(face_info)

        # Store in Neo4j
        store_metadata_to_neo4j(caption, face_info.get("age"), face_info.get("gender"))
        log_metadata(caption, face_info)

        return {
            "caption": caption,
            "face_info": face_info
        }
    except Exception as e:
        error_info = {"error": str(e)}
        log_metadata("Error processing image", error_info)
        return error_info
