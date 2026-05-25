"""
Soil Image Analysis Service
Uses Google Gemini Vision API (FREE) to analyze soil images.
"""
import base64
import json
import os
import re


def analyze_soil_image(image_path: str) -> dict:
    api_key = os.environ.get('GEMINI_API_KEY', '')
    if not api_key:
        return {
            'error': 'GEMINI_API_KEY not configured. Set it in Render environment variables.',
            'success': False
        }

    try:
        import google.generativeai as genai
        from PIL import Image
    except ImportError:
        return {'error': 'google-generativeai or Pillow not installed.', 'success': False}

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        img = Image.open(image_path)

        prompt = """You are an expert soil scientist and agronomist. Analyze this soil/land image thoroughly.

Return ONLY a valid JSON object (no markdown, no extra text) with exactly these fields:

{
  "soil_type": "e.g. Alluvial Soil / Black Cotton Soil / Red Soil / Laterite / Loamy / Sandy / Clay",
  "texture": "e.g. Sandy Loam / Clay Loam / Silty Clay / Sandy / Loamy / Heavy Clay",
  "color_analysis": "description of soil color and what it indicates",
  "ph_estimate": 6.8,
  "ph_category": "Neutral",
  "moisture_estimate": 45,
  "nitrogen_level": "Low / Medium / High",
  "phosphorus_level": "Low / Medium / High",
  "potassium_level": "Low / Medium / High",
  "organic_matter": "Low / Medium / High",
  "quality": "Excellent / Good / Average / Poor",
  "health_score": 72,
  "suitable_crops": ["Wheat", "Rice", "Maize", "Soybean", "Cotton"],
  "not_suitable_crops": ["Blueberry", "Tea"],
  "fertilizer_recommendations": [
    "Apply NPK 10-26-26 at 100 kg/acre",
    "Add 2 tonnes/acre of farmyard manure"
  ],
  "irrigation_advice": "Drip irrigation recommended",
  "soil_improvement": [
    "Add organic compost to improve structure",
    "Consider green manuring with legumes"
  ],
  "issues": ["Low organic matter", "Slight compaction visible"],
  "strengths": ["Good texture", "Adequate drainage"],
  "season_recommendations": {
    "Kharif (June-Oct)": ["Rice", "Maize", "Cotton"],
    "Rabi (Nov-Mar)": ["Wheat", "Barley", "Mustard"],
    "Zaid (Mar-Jun)": ["Watermelon", "Cucumber"]
  },
  "summary": "2-3 sentence overall assessment and primary recommendations"
}

Base your analysis on visual cues: color, texture, structure, moisture. Be specific and practical for Indian farming."""

        response = model.generate_content([prompt, img])
        raw = response.text.strip()

        # Strip markdown fences
        raw = re.sub(r'^```(?:json)?\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw)

        result = json.loads(raw)
        result['success'] = True
        return result

    except json.JSONDecodeError:
        try:
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                result = json.loads(match.group())
                result['success'] = True
                return result
        except Exception:
            pass
        return {'error': 'Could not parse AI response', 'success': False}
    except Exception as e:
        return {'error': f'Analysis failed: {str(e)}', 'success': False}
