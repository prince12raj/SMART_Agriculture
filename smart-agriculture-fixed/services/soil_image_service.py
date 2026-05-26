"""
Soil Image Analysis Service
Uses gradio_client to call CNN on HuggingFace Space.
"""
import os
import base64
import tempfile
from PIL import Image

HF_SPACE = "prince12raj/soil-analysis-api"

SOIL_CROPS = {
    "Black_Soil":    ["Cotton", "Soybean", "Wheat", "Sugarcane"],
    "Red_Soil":      ["Groundnut", "Millets", "Potato", "Rice"],
    "Alluvial_Soil": ["Rice", "Sugarcane", "Wheat", "Maize"],
    "Arid_Soil":     ["Barley", "Millets", "Maize"],
    "Laterite_Soil": ["Tea", "Coffee", "Rubber", "Coconut"],
    "Mountain_Soil": ["Tea", "Coffee", "Spices", "Apple"],
    "Yellow_Soil":   ["Groundnut", "Potato", "Rice"],
}

SOIL_NUTRIENTS = {
    "Black_Soil":    ["Potassium", "Lime", "Iron"],
    "Red_Soil":      ["Nitrogen", "Phosphorus", "Organic Compost"],
    "Alluvial_Soil": ["Potash", "Phosphorus", "Humus"],
    "Arid_Soil":     ["Organic Matter", "Nitrogen"],
    "Laterite_Soil": ["Lime", "Phosphate", "Organic Fertilizer"],
    "Mountain_Soil": ["Humus", "Nitrogen", "Organic Compost"],
    "Yellow_Soil":   ["Nitrogen", "Organic Matter"],
}

SOIL_INFO = {
    "Black_Soil":    {"quality":"Good",      "ph_estimate":7.5,"ph_category":"Slightly Alkaline","moisture_estimate":55,"nitrogen_level":"Medium","phosphorus_level":"Low",   "potassium_level":"High",  "organic_matter":"High",  "health_score":78,"irrigation_advice":"Moderate irrigation. Avoid waterlogging.","soil_improvement":["Add phosphorus fertilizer","Deep ploughing recommended"],"issues":["Low phosphorus","Heavy when wet"],"strengths":["High potassium","Good moisture retention"]},
    "Red_Soil":      {"quality":"Average",   "ph_estimate":6.2,"ph_category":"Slightly Acidic",  "moisture_estimate":35,"nitrogen_level":"Low",   "phosphorus_level":"Low",   "potassium_level":"Medium","organic_matter":"Low",   "health_score":58,"irrigation_advice":"Regular irrigation needed.","soil_improvement":["Add organic compost","Apply NPK fertilizer"],"issues":["Low nitrogen","Poor water retention"],"strengths":["Good drainage","Easy to till"]},
    "Alluvial_Soil": {"quality":"Excellent", "ph_estimate":7.0,"ph_category":"Neutral",          "moisture_estimate":60,"nitrogen_level":"High",  "phosphorus_level":"High",  "potassium_level":"High",  "organic_matter":"High",  "health_score":92,"irrigation_advice":"Canal and drip irrigation both work well.","soil_improvement":["Maintain organic matter","Crop rotation essential"],"issues":["Needs drainage in flood areas"],"strengths":["Highly fertile","Rich in all nutrients"]},
    "Arid_Soil":     {"quality":"Poor",      "ph_estimate":8.0,"ph_category":"Alkaline",         "moisture_estimate":15,"nitrogen_level":"Low",   "phosphorus_level":"Low",   "potassium_level":"Medium","organic_matter":"Low",   "health_score":35,"irrigation_advice":"Drip irrigation essential. Use mulching.","soil_improvement":["Heavy organic matter","Mulching compulsory","Gypsum for salinity"],"issues":["High salinity","Very low moisture"],"strengths":["Good for drought crops"]},
    "Laterite_Soil": {"quality":"Average",   "ph_estimate":5.5,"ph_category":"Acidic",           "moisture_estimate":40,"nitrogen_level":"Low",   "phosphorus_level":"Low",   "potassium_level":"Low",   "organic_matter":"Medium","health_score":52,"irrigation_advice":"Moderate irrigation. Prone to leaching.","soil_improvement":["Apply lime","Add phosphate fertilizer"],"issues":["High acidity","Low nutrient retention"],"strengths":["Good for plantations","Well-drained"]},
    "Mountain_Soil": {"quality":"Good",      "ph_estimate":5.8,"ph_category":"Slightly Acidic",  "moisture_estimate":50,"nitrogen_level":"Medium","phosphorus_level":"Medium","potassium_level":"Low",   "organic_matter":"High",  "health_score":70,"irrigation_advice":"Rainfall usually sufficient. Build terraces.","soil_improvement":["Add potassium fertilizer","Build terraces"],"issues":["Erosion prone","Shallow depth"],"strengths":["Rich in humus","Good for spices"]},
    "Yellow_Soil":   {"quality":"Average",   "ph_estimate":6.5,"ph_category":"Slightly Acidic",  "moisture_estimate":38,"nitrogen_level":"Low",   "phosphorus_level":"Medium","potassium_level":"Low",   "organic_matter":"Low",   "health_score":55,"irrigation_advice":"Moderate irrigation needed.","soil_improvement":["Add nitrogen fertilizer","Use green manuring"],"issues":["Low nitrogen","Low organic matter"],"strengths":["Workable texture","Responds to fertilizers"]},
}

SEASON_RECS = {
    "Black_Soil":    {"Kharif (June-Oct)":["Cotton","Soybean","Maize"],    "Rabi (Nov-Mar)":["Wheat","Gram","Mustard"],   "Zaid (Mar-Jun)":["Sugarcane","Vegetables"]},
    "Red_Soil":      {"Kharif (June-Oct)":["Groundnut","Rice","Millets"],  "Rabi (Nov-Mar)":["Potato","Wheat"],          "Zaid (Mar-Jun)":["Watermelon","Cucumber"]},
    "Alluvial_Soil": {"Kharif (June-Oct)":["Rice","Maize","Cotton"],       "Rabi (Nov-Mar)":["Wheat","Barley","Mustard"],"Zaid (Mar-Jun)":["Sugarcane","Vegetables"]},
    "Arid_Soil":     {"Kharif (June-Oct)":["Millets","Maize"],             "Rabi (Nov-Mar)":["Barley","Gram"],           "Zaid (Mar-Jun)":["Watermelon"]},
    "Laterite_Soil": {"Kharif (June-Oct)":["Rice","Rubber","Coconut"],     "Rabi (Nov-Mar)":["Coffee","Tea"],            "Zaid (Mar-Jun)":["Cashew","Mango"]},
    "Mountain_Soil": {"Kharif (June-Oct)":["Tea","Spices","Maize"],        "Rabi (Nov-Mar)":["Apple","Potato"],          "Zaid (Mar-Jun)":["Coffee","Cardamom"]},
    "Yellow_Soil":   {"Kharif (June-Oct)":["Groundnut","Rice"],            "Rabi (Nov-Mar)":["Potato","Wheat"],          "Zaid (Mar-Jun)":["Watermelon","Vegetables"]},
}


def analyze_soil_image(image_path: str) -> dict:
    try:
        from gradio_client import Client, handle_file

        client = Client(HF_SPACE)
        result_text = client.predict(
            image=handle_file(image_path),
            api_name="/predict"
        )

        # Parse soil type from result text
        soil_type  = None
        confidence = 0.0

        for line in result_text.split('\n'):
            if 'Soil Type' in line and ':' in line:
                val = line.split(':', 1)[1].strip().replace(' ', '_')
                if val in SOIL_INFO:
                    soil_type = val
            if 'Confidence' in line and ':' in line:
                try:
                    confidence = float(line.split(':', 1)[1].strip().replace('%', ''))
                except Exception:
                    pass

        # Fallback — scan text for known soil names
        if not soil_type:
            for key in SOIL_INFO:
                if key.replace('_', ' ').lower() in result_text.lower():
                    soil_type = key
                    break

        if not soil_type:
            return {'error': f'Could not parse soil type from: {result_text[:200]}', 'success': False}

        info    = SOIL_INFO[soil_type]
        crops   = SOIL_CROPS[soil_type]
        nuts    = SOIL_NUTRIENTS[soil_type]
        seasons = SEASON_RECS[soil_type]

        return {
            'success':                  True,
            'soil_type':                soil_type.replace('_', ' '),
            'texture':                  'Medium Loam',
            'color_analysis':           f'CNN model confirmed {soil_type.replace("_"," ")} characteristics',
            'ph_estimate':              info['ph_estimate'],
            'ph_category':              info['ph_category'],
            'moisture_estimate':        info['moisture_estimate'],
            'nitrogen_level':           info['nitrogen_level'],
            'phosphorus_level':         info['phosphorus_level'],
            'potassium_level':          info['potassium_level'],
            'organic_matter':           info['organic_matter'],
            'quality':                  info['quality'],
            'health_score':             info['health_score'],
            'confidence':               round(confidence, 2),
            'suitable_crops':           crops,
            'not_suitable_crops':       [],
            'fertilizer_recommendations': [f'Apply {n}' for n in nuts],
            'irrigation_advice':        info['irrigation_advice'],
            'soil_improvement':         info['soil_improvement'],
            'issues':                   info['issues'],
            'strengths':                info['strengths'],
            'season_recommendations':   seasons,
            'summary':                  f'CNN identified {soil_type.replace("_"," ")} with {confidence:.1f}% confidence. '
                                        f'Quality: {info["quality"]}. Best crops: {", ".join(crops[:3])}.'
        }

    except Exception as e:
        return {'error': f'Analysis failed: {str(e)}', 'success': False}
