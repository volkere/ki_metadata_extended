import torch
from transformers import CLIPProcessor, CLIPModel
from deepface import DeepFace
from PIL import Image
import io
from neo4j import GraphDatabase
from app.utils.logger import log_metadata

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

NEO4J_URI = "bolt://neo4j:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

def store_metadata_to_neo4j(caption, age, gender):
    with driver.session() as session:
        session.run(
            "MERGE (d:Description {text: $caption}) "
            "MERGE (p:Person {age: $age, gender: $gender}) "
            "MERGE (d)-[:DESCRIBES]->(p)",
            caption=caption, age=age, gender=gender
        )

def process_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    inputs = clip_processor(text=["a photo", "a person", "a performance"], images=image, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1).tolist()[0]
    labels = ["a photo", "a person", "a performance"]
    caption = labels[probs.index(max(probs))]

    try:
        face_result = DeepFace.analyze(img_path=image, actions=['age', 'gender'], enforce_detection=False)
        face_info = face_result[0] if isinstance(face_result, list) else face_result
    except Exception as e:
        face_info = {"error": str(e)}

    store_metadata_to_neo4j(caption, face_info.get("age"), face_info.get("gender"))
    log_metadata(caption, face_info)

    return {
        "caption": caption,
        "face_info": face_info
    }
