import os
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def normalize_value(value, min_val, max_val):
    """Normalize a value to 0-1 range"""
    if max_val == min_val:
        return 0
    return (value - min_val) / (max_val - min_val)

def preprocess_image(image_path, target_size=(224, 224)):
    """Preprocess image for ML model input"""
    try:
        from PIL import Image
        import numpy as np
        img = Image.open(image_path).convert('RGB')
        img = img.resize(target_size)
        img_array = np.array(img) / 255.0
        return img_array
    except Exception as e:
        raise ValueError(f"Image preprocessing failed: {str(e)}")

def clean_text(text):
    """Basic text sanitization"""
    if not text:
        return ''
    return str(text).strip()[:500]
