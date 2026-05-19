"""
AI-powered land image analysis using Anthropic Claude vision API.
"""
import os, base64, json, re
from flask import current_app


def analyze_land_image(image_path: str) -> dict:
    """
    Send land image to Claude API for soil analysis.
    Returns pH, NPK, organic matter, moisture, health score, crops, etc.
    Falls back to rule-based demo if API key not set.
    """
    api_key = current_app.config.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        return _demo_analysis()

    try:
        import requests as req

        with open(image_path, 'rb') as f:
            b64_data = base64.b64encode(f.read()).decode('utf-8')

        ext = image_path.rsplit('.', 1)[-1].lower()
        media_map = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
                     'png': 'image/png', 'webp': 'image/webp', 'gif': 'image/gif'}
        media_type = media_map.get(ext, 'image/jpeg')

        prompt = (
            "You are an expert agricultural soil scientist. Analyze this land/soil image "
            "and return ONLY a JSON object with no markdown, no backticks:\n"
            '{"ph":<4.0-9.0>,"nitrogen":<0-100>,"phosphorus":<0-100>,"potassium":<0-100>,'
            '"organicMatter":<0-10>,"moisture":<0-100>,"healthScore":<0-100>,'
            '"soilColor":"<color>","texture":"<sandy/loamy/clay/silt>",'
            '"quality":"<Excellent/Good/Average/Poor>",'
            '"suitableCrops":["crop1","crop2","crop3","crop4"],'
            '"fertilizer":"<recommendation>","irrigation":"<advice>",'
            '"issues":["issue1"],"summary":"<2 sentence assessment>"}'
        )

        response = req.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01'
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 1000,
                'messages': [{
                    'role': 'user',
                    'content': [
                        {'type': 'image', 'source': {
                            'type': 'base64',
                            'media_type': media_type,
                            'data': b64_data
                        }},
                        {'type': 'text', 'text': prompt}
                    ]
                }]
            },
            timeout=30
        )

        data = response.json()
        text = ''.join(
            block.get('text', '')
            for block in data.get('content', [])
            if block.get('type') == 'text'
        )
        text = re.sub(r'```json|```', '', text).strip()
        return json.loads(text)

    except Exception as e:
        result = _demo_analysis()
        result['note'] = f'AI unavailable ({e}), showing demo result'
        return result


def _demo_analysis() -> dict:
    """Rule-based demo when API key is not configured"""
    return {
        'ph': 6.8,
        'nitrogen': 62,
        'phosphorus': 48,
        'potassium': 55,
        'organicMatter': 3.2,
        'moisture': 45,
        'healthScore': 72,
        'soilColor': 'Dark brown',
        'texture': 'loamy',
        'quality': 'Good',
        'suitableCrops': ['Wheat', 'Rice', 'Maize', 'Pulses'],
        'fertilizer': 'Apply DAP at 50 kg/acre before sowing. Top-dress with urea at 30 kg/acre.',
        'irrigation': 'Drip irrigation recommended. Water every 5-7 days. Avoid waterlogging.',
        'issues': ['Slightly low phosphorus', 'Monitor moisture levels'],
        'summary': 'Soil appears to be in good condition with balanced NPK levels. '
                   'Minor phosphorus supplementation is recommended for optimal yield.',
        'note': 'Demo result — add ANTHROPIC_API_KEY to config for real AI analysis'
    }