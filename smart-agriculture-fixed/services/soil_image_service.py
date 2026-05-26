"""
Soil Image Analysis Service
Calls CNN model hosted on Hugging Face Space:
https://prince12raj-soil-analysis-api.hf.space/
"""
import os
import json
import base64
import requests
from PIL import Image
import io

HF_API_URL = "https://prince12raj-soil-analysis-api.hf.space/gradio/api/predict"

SOIL_INFO = {
    "Black_Soil":    {
        "quality": "Good", "ph_estimate": 7.5, "ph_category": "Slightly Alkaline",
        "moisture_estimate": 55, "nitrogen_level": "Medium", "phosphorus_level": "Low",
        "potassium_level": "High", "organic_matter": "High", "health_score": 78,
        "irrigation_advice": "Moderate irrigation. Avoid waterlogging as black soil retains water.",
        "soil_improvement": ["Add phosphorus fertilizer", "Avoid over-irrigation", "Deep ploughing recommended"],
        "issues": ["Low phosphorus", "Heavy and sticky when wet", "Prone to cracking when dry"],
        "strengths": ["High potassium", "Good moisture retention", "Rich in calcium and magnesium"]
    },
    "Red_Soil":      {
        "quality": "Average", "ph_estimate": 6.2, "ph_category": "Slightly Acidic",
        "moisture_estimate": 35, "nitrogen_level": "Low", "phosphorus_level": "Low",
        "potassium_level": "Medium", "organic_matter": "Low", "health_score": 58,
        "irrigation_advice": "Regular irrigation needed. Poor moisture retention.",
        "soil_improvement": ["Add organic compost", "Apply NPK fertilizer regularly", "Mulching to retain moisture"],
        "issues": ["Low nitrogen and phosphorus", "Poor water retention", "Iron and aluminium compounds"],
        "strengths": ["Good drainage", "Easy to till", "Responds well to fertilizers"]
    },
    "Alluvial_Soil": {
        "quality": "Excellent", "ph_estimate": 7.0, "ph_category": "Neutral",
        "moisture_estimate": 60, "nitrogen_level": "High", "phosphorus_level": "High",
        "potassium_level": "High", "organic_matter": "High", "health_score": 92,
        "irrigation_advice": "High irrigation capacity. Canal and drip irrigation both work well.",
        "soil_improvement": ["Maintain organic matter", "Crop rotation is essential", "Avoid soil compaction"],
        "issues": ["May need drainage management in flood-prone areas"],
        "strengths": ["Highly fertile", "Rich in all nutrients", "Best agricultural soil in India"]
    },
    "Arid_Soil":     {
        "quality": "Poor", "ph_estimate": 8.0, "ph_category": "Alkaline",
        "moisture_estimate": 15, "nitrogen_level": "Low", "phosphorus_level": "Low",
        "potassium_level": "Medium", "organic_matter": "Low", "health_score": 35,
        "irrigation_advice": "Drip irrigation essential. Use mulching to minimize water loss.",
        "soil_improvement": ["Heavy organic matter addition", "Mulching compulsory", "Gypsum for salinity treatment"],
        "issues": ["Very high salinity", "Extremely low moisture", "Low organic matter", "Infertile"],
        "strengths": ["Good for drought-resistant crops", "Mineral-rich subsoil"]
    },
    "Laterite_Soil": {
        "quality": "Average", "ph_estimate": 5.5, "ph_category": "Acidic",
        "moisture_estimate": 40, "nitrogen_level": "Low", "phosphorus_level": "Low",
        "potassium_level": "Low", "organic_matter": "Medium", "health_score": 52,
        "irrigation_advice": "Moderate irrigation. Prone to nutrient leaching after heavy rain.",
        "soil_improvement": ["Apply lime to reduce acidity", "Add phosphate fertilizer", "Heavy organic compost"],
        "issues": ["High acidity", "Low nutrient retention", "Iron and aluminium toxicity"],
        "strengths": ["Good for plantation crops", "Well-drained", "Suitable for hilly terrain"]
    },
    "Mountain_Soil": {
        "quality": "Good", "ph_estimate": 5.8, "ph_category": "Slightly Acidic",
        "moisture_estimate": 50, "nitrogen_level": "Medium", "phosphorus_level": "Medium",
        "potassium_level": "Low", "organic_matter": "High", "health_score": 70,
        "irrigation_advice": "Natural rainfall usually sufficient. Terracing prevents erosion.",
        "soil_improvement": ["Add potassium fertilizer", "Build terraces on slopes", "Prevent soil erosion"],
        "issues": ["Low potassium", "Erosion prone on steep slopes", "Shallow depth"],
        "strengths": ["Rich in humus", "Good for tea and spices", "Natural moisture retention"]
    },
    "Yellow_Soil":   {
        "quality": "Average", "ph_estimate": 6.5, "ph_category": "Slightly Acidic",
        "moisture_estimate": 38, "nitrogen_level": "Low", "phosphorus_level": "Medium",
        "potassium_level": "Low", "organic_matter": "Low", "health_score": 55,
        "irrigation_advice": "Moderate irrigation. Improve water retention with organic compost.",
        "soil_improvement": ["Add nitrogen fertilizer", "Organic matter is essential", "Use green manuring"],
        "issues": ["Low nitrogen", "Low organic matter", "Moderate leaching"],
        "strengths": ["Moderate drainage", "Workable texture", "Responds to fertilizers"]
    },
}

SEASON_RECS = {
    "Black_Soil":    {"Kharif (June-Oct)": ["Cotton", "Soybean", "Maize"],     "Rabi (Nov-Mar)": ["Wheat", "Gram", "Mustard"],      "Zaid (Mar-Jun)": ["Sugarcane", "Vegetables"]},
    "Red_Soil":      {"Kharif (June-Oct)": ["Groundnut", "Rice", "Millets"],   "Rabi (Nov-Mar)": ["Potato", "Wheat"],               "Zaid (Mar-Jun)": ["Watermelon", "Cucumber"]},
    "Alluvial_Soil": {"Kharif (June-Oct)": ["Rice", "Maize", "Cotton"],        "Rabi (Nov-Mar)": ["Wheat", "Barley", "Mustard"],    "Zaid (Mar-Jun)": ["Sugarcane", "Vegetables"]},
    "Arid_Soil":     {"Kharif (June-Oct)": ["Millets", "Maize"],               "Rabi (Nov-Mar)": ["Barley", "Gram"],                "Zaid (Mar-Jun)": ["Watermelon"]},
    "Laterite_Soil": {"Kharif (June-Oct)": ["Rice", "Rubber", "Coconut"],      "Rabi (Nov-Mar)": ["Coffee", "Tea"],                 "Zaid (Mar-Jun)": ["Cashew", "Mango"]},
    "Mountain_Soil": {"Kharif (June-Oct)": ["Tea", "Spices", "Maize"],         "Rabi (Nov-Mar)": ["Apple", "Potato"],               "Zaid (Mar-Jun)": ["Coffee", "Cardamom"]},
    "Yellow_Soil":   {"Kharif (June-Oct)": ["Groundnut", "Rice"],              "Rabi (Nov-Mar)": ["Potato", "Wheat"],               "Zaid (Mar-Jun)": ["Watermelon", "Vegetables"]},
}


def analyze_soil_image(image_path: str) -> dict:
    try:
        # Read and encode image as base64
        with open(image_path, 'rb') as f:
            img_bytes = f.read()

        # Convert to base64 for Gradio API
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')

        # Detect media type
        ext = os.path.splitext(image_path)[1].lower()
        media_map = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                     '.png': 'image/png', '.webp': 'image/webp'}
        media_type = media_map.get(ext, 'image/jpeg')

        # Call Gradio API
        payload = {
            "data": [
                {
                    "data": f"data:{media_type};base64,{img_b64}",
                    "mime_type": media_type
                }
            ]
        }

        response = requests.post(HF_API_URL, json=payload, timeout=60)

        if response.status_code != 200:
            return {'error': f'HuggingFace API error {response.status_code}: {response.text[:200]}', 'success': False}

        result_data = response.json()

        # Parse the text output from Gradio
        raw_text = ""
        if "data" in result_data and len(result_data["data"]) > 0:
            raw_text = result_data["data"][0]
        elif "output" in result_data:
            raw_text = str(result_data["output"])

        if not raw_text:
            return {'error': 'Empty response from CNN API', 'success': False}

        # Parse soil type and confidence from text output
        soil_type  = None
        confidence = 0.0

        for line in raw_text.split('\n'):
            if 'Soil Type' in line and ':' in line:
                val = line.split(':', 1)[1].strip()
                # Convert display name back to key
                soil_type = val.replace(' ', '_')
            if 'Confidence' in line and ':' in line:
                val = line.split(':', 1)[1].strip().replace('%', '')
                try:
                    confidence = float(val)
                except Exception:
                    pass

        if not soil_type or soil_type not in SOIL_INFO:
            # Try matching partial
            for key in SOIL_INFO:
                if key.lower().replace('_', '') in raw_text.lower().replace(' ', ''):
                    soil_type = key
                    break

        if not soil_type:
            return {'error': f'Could not parse soil type from response:\n{raw_text[:300]}', 'success': False}

        info    = SOIL_INFO[soil_type]
        seasons = SEASON_RECS[soil_type]
        crops   = SOIL_INFO[soil_type].get('crops', [])

        # Get crops from soil_info keys
        soil_crops_map = {
            "Black_Soil":    ["Cotton", "Soybean", "Wheat", "Sugarcane"],
            "Red_Soil":      ["Groundnut", "Millets", "Potato", "Rice"],
            "Alluvial_Soil": ["Rice", "Sugarcane", "Wheat", "Maize"],
            "Arid_Soil":     ["Barley", "Millets", "Maize"],
            "Laterite_Soil": ["Tea", "Coffee", "Rubber", "Coconut"],
            "Mountain_Soil": ["Tea", "Coffee", "Spices", "Apple"],
            "Yellow_Soil":   ["Groundnut", "Potato", "Rice"],
        }
        suitable_crops = soil_crops_map.get(soil_type, [])

        display_name = soil_type.replace('_', ' ')

        return {
            'success':                  True,
            'soil_type':                display_name,
            'texture':                  'Medium Loam',
            'color_analysis':           f'Visual CNN analysis confirmed {display_name} characteristics',
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
            'suitable_crops':           suitable_crops,
            'not_suitable_crops':       [],
            'fertilizer_recommendations': [f'Apply {n} fertilizer as needed' for n in
                                          {"Black_Soil": ["Potassium","Lime","Iron"],
                                           "Red_Soil":   ["Nitrogen","Phosphorus","Organic Compost"],
                                           "Alluvial_Soil": ["Potash","Phosphorus","Humus"],
                                           "Arid_Soil":  ["Organic Matter","Nitrogen"],
                                           "Laterite_Soil": ["Lime","Phosphate","Organic Fertilizer"],
                                           "Mountain_Soil": ["Humus","Nitrogen","Organic Compost"],
                                           "Yellow_Soil": ["Nitrogen","Organic Matter"]
                                           }.get(soil_type, [])],
            'irrigation_advice':        info['irrigation_advice'],
            'soil_improvement':         info['soil_improvement'],
            'issues':                   info['issues'],
            'strengths':                info['strengths'],
            'season_recommendations':   seasons,
            'summary':                  f'CNN model identified {display_name} with {confidence:.1f}% confidence. '
                                        f'Quality: {info["quality"]}. '
                                        f'Best crops: {", ".join(suitable_crops[:3])}. '
                                        f'pH range: {info["ph_category"]}.'
        }

    except requests.exceptions.Timeout:
        return {'error': 'HuggingFace Space timed out. It may be starting up — try again in 30 seconds.', 'success': False}
    except requests.exceptions.ConnectionError:
        return {'error': 'Cannot connect to HuggingFace Space. Please check if it is running.', 'success': False}
    except Exception as e:
        return {'error': f'Analysis failed: {str(e)}', 'success': False}
