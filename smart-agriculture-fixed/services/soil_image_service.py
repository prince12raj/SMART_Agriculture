"""
Soil Image Analysis Service
Uses Claude Vision API to analyze soil/land images and return
detailed soil quality report with crop recommendations.
"""
import base64
import json
import os
import re

def analyze_soil_image(image_path: str) -> dict:
    """
    Analyze a soil image using Claude Vision API.
    Returns structured soil analysis results.
    """
    try:
        import anthropic
    except ImportError:
        return _fallback_analysis()

    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        return _fallback_analysis()

    # Read and encode the image
    try:
        with open(image_path, 'rb') as f:
            image_data = base64.standard_b64encode(f.read()).decode('utf-8')
    except Exception as e:
        return {'error': f'Could not read image: {str(e)}'}

    # Detect media type
    ext = os.path.splitext(image_path)[1].lower()
    media_map = {
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.png': 'image/png', '.webp': 'image/webp',
        '.gif': 'image/gif'
    }
    media_type = media_map.get(ext, 'image/jpeg')

    prompt = """You are an expert soil scientist and agronomist. Analyze this soil/land image thoroughly.

Return ONLY a valid JSON object (no markdown, no extra text) with exactly these fields:

{
  "soil_type": "e.g. Alluvial Soil / Black Cotton Soil / Red Soil / Laterite / Loamy / Sandy / Clay / Mixed",
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
    "Apply NPK 10-26-26 at 100 kg/acre for phosphorus boost",
    "Add 2 tonnes/acre of well-composted farmyard manure"
  ],
  "irrigation_advice": "Drip irrigation recommended due to moderate moisture retention",
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
  "summary": "2-3 sentence overall assessment of the soil quality and primary recommendations"
}

Base your analysis on visual cues: color (dark = high organic matter, red = iron-rich, grey = poor drainage), texture, visible structure, moisture, any visible roots or organisms. Be specific and practical for Indian farming context."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )

        raw = response.content[0].text.strip()
        # Strip markdown code fences if present
        raw = re.sub(r'^```(?:json)?\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw)

        result = json.loads(raw)
        result['success'] = True
        return result

    except json.JSONDecodeError:
        # Try to extract JSON from the response
        try:
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                result = json.loads(match.group())
                result['success'] = True
                return result
        except Exception:
            pass
        return {'error': 'Could not parse AI response', 'raw': raw[:500]}
    except Exception as e:
        return {'error': f'Analysis failed: {str(e)}'}


def _fallback_analysis():
    """Return a message when API key is not configured."""
    return {
        'error': 'ANTHROPIC_API_KEY not configured. Please set it in your environment variables on Render.',
        'success': False
    }
