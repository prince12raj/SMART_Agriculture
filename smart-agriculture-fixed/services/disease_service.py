import os
# NEW - safe import
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# Disease database with solutions
DISEASE_DATABASE = {
    'Tomato_Early_Blight': {
        'disease': 'Tomato Early Blight',
        'solution': 'Remove infected leaves. Apply copper-based fungicide. Avoid overhead irrigation. Rotate crops annually.',
        'severity': 'Moderate'
    },
    'Tomato_Late_Blight': {
        'disease': 'Tomato Late Blight',
        'solution': 'Apply Mancozeb or Chlorothalonil fungicide. Remove and destroy infected plants. Improve air circulation.',
        'severity': 'Severe'
    },
    'Corn_Common_Rust': {
        'disease': 'Corn Common Rust',
        'solution': 'Apply fungicide like Propiconazole. Plant resistant varieties. Monitor fields regularly.',
        'severity': 'Moderate'
    },
    'Potato_Late_Blight': {
        'disease': 'Potato Late Blight',
        'solution': 'Spray with Ridomil Gold or Revus. Remove infected plants. Ensure good field drainage.',
        'severity': 'Severe'
    },
    'Rice_Blast': {
        'disease': 'Rice Blast',
        'solution': 'Apply Tricyclazole or Carbendazim. Reduce nitrogen application. Plant blast-resistant varieties.',
        'severity': 'Severe'
    },
    'Wheat_Yellow_Rust': {
        'disease': 'Wheat Yellow Rust (Stripe Rust)',
        'solution': 'Apply Tebuconazole fungicide. Plant resistant varieties. Early sowing to avoid peak rust season.',
        'severity': 'Severe'
    },
    'Healthy': {
        'disease': 'No Disease Detected',
        'solution': 'Plant appears healthy. Continue regular monitoring and good agricultural practices.',
        'severity': 'None'
    }
}

def detect_disease(image_path, crop_name='Unknown'):
    """
    Detect crop disease from image.
    Uses pre-trained DL model if available, otherwise returns demo result.
    """
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'disease_model.h5')

    if os.path.exists(model_path):
        try:
            import tensorflow as tf
            from PIL import Image

            model = tf.keras.models.load_model(model_path)
            img = Image.open(image_path).resize((224, 224))
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            predictions = model.predict(img_array)
            class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][class_idx])

            classes = list(DISEASE_DATABASE.keys())
            if class_idx < len(classes):
                disease_key = classes[class_idx]
            else:
                disease_key = 'Healthy'

            disease_info = DISEASE_DATABASE[disease_key]
            return {
                'disease': disease_info['disease'],
                'solution': disease_info['solution'],
                'severity': disease_info['severity'],
                'confidence': round(confidence * 100, 2),
                'crop': crop_name
            }
        except Exception as e:
            return _demo_result(crop_name, str(e))
    else:
        return _demo_result(crop_name)

def _demo_result(crop_name, note='Model not loaded - showing demo result'):
    """Demo result when model is not available"""
    import random
    diseases = [
        ('Early Blight', 'Apply copper-based fungicide. Remove infected leaves. Avoid overhead watering.', 'Moderate', 87.3),
        ('Powdery Mildew', 'Apply sulfur-based fungicide. Improve air circulation. Reduce humidity.', 'Mild', 79.1),
        ('Healthy', 'No disease detected. Continue good agricultural practices.', 'None', 95.4)
    ]
    d = random.choice(diseases)
    return {
        'disease': d[0],
        'solution': d[1],
        'severity': d[2],
        'confidence': d[3],
        'crop': crop_name,
        'note': note
    }
