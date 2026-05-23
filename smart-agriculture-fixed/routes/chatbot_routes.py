from flask import Blueprint, request, jsonify, session
from functools import wraps
import os, anthropic

chatbot_bp = Blueprint('chatbot', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Login required'}), 401
        return f(*args, **kwargs)
    return decorated

SYSTEM_PROMPT = """You are AgriBot, a friendly and knowledgeable farming assistant for Indian farmers.
You help with:
- Soil health, crop selection, fertilizers, irrigation
- Pest and disease identification and treatment
- Seasonal farming advice (Kharif, Rabi, Zaid)
- Market prices and selling tips
- Government schemes for farmers (PM-KISAN, soil health card, etc.)
- Weather-based farming decisions
- Storage and post-harvest tips

Rules:
- Detect if the user writes in Hindi (Devanagari script) and reply fully in Hindi.
- If user writes in English, reply in English.
- If mixed, reply in Hindi-English mix (Hinglish).
- Keep answers practical, simple, and specific to Indian farming.
- Use bullet points for lists. Be concise — 3-5 sentences max unless detail is needed.
- Always be warm and encouraging. Address the farmer respectfully.
- Never give medical advice unrelated to farming.
"""

@chatbot_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    messages = data.get('messages', [])

    if not messages:
        return jsonify({'error': 'No messages provided'}), 400

    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 500

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=messages
        )
        reply = response.content[0].text
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
