import os
try:
    import joblib
    import numpy as np
    HAS_ML = True
except ImportError:
    HAS_ML = False

# Crop recommendations based on soil conditions
CROP_RECOMMENDATIONS = {
    'Acidic': ['Tea', 'Coffee', 'Potato', 'Blueberry', 'Strawberry'],
    'Slightly Acidic': ['Rice', 'Maize', 'Wheat', 'Sugarcane', 'Groundnut'],
    'Neutral': ['Wheat', 'Barley', 'Lettuce', 'Spinach', 'Beans'],
    'Slightly Alkaline': ['Cotton', 'Barley', 'Sugarbeet', 'Alfalfa'],
    'Alkaline': ['Asparagus', 'Celery', 'Cabbage', 'Cauliflower']
}

NUTRIENT_CROPS = {
    'high_n': ['Leafy Greens', 'Maize', 'Wheat', 'Sugarcane'],
    'high_p': ['Tomato', 'Pepper', 'Carrot', 'Radish'],
    'high_k': ['Potato', 'Banana', 'Coconut', 'Sugarcane']
}

def get_ph_category(ph):
    if ph < 5.5:
        return 'Acidic'
    elif ph < 6.5:
        return 'Slightly Acidic'
    elif ph < 7.5:
        return 'Neutral'
    elif ph < 8.5:
        return 'Slightly Alkaline'
    else:
        return 'Alkaline'

def analyze_soil(params):
    """
    Analyze soil parameters and return quality report + recommendations.
    Uses pre-trained ML model if available, falls back to rule-based system.
    """
    ph = params.get('ph', 7.0)
    moisture = params.get('moisture', 50.0)
    nitrogen = params.get('nitrogen', 50.0)
    phosphorus = params.get('phosphorus', 50.0)
    potassium = params.get('potassium', 50.0)

    # Try loading ML model
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'soil_model.pkl')
    if HAS_ML and os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            features = np.array([[nitrogen, phosphorus, potassium, ph, moisture]])
            prediction = model.predict(features)[0]
            quality = 'Good' if prediction == 1 else 'Needs Improvement'
        except Exception:
            quality = _rule_based_quality(ph, moisture, nitrogen, phosphorus, potassium)
    else:
        quality = _rule_based_quality(ph, moisture, nitrogen, phosphorus, potassium)

    ph_category = get_ph_category(ph)
    recommended_crops = CROP_RECOMMENDATIONS.get(ph_category, ['Wheat', 'Rice'])

    # Add nutrient-based recommendations
    if nitrogen > 60:
        recommended_crops += NUTRIENT_CROPS['high_n'][:2]
    if phosphorus > 60:
        recommended_crops += NUTRIENT_CROPS['high_p'][:2]
    if potassium > 60:
        recommended_crops += NUTRIENT_CROPS['high_k'][:2]

    recommended_crops = list(set(recommended_crops))[:6]

    issues = []
    suggestions = []
    if ph < 6.0:
        issues.append('Low pH (Acidic)')
        suggestions.append('Add agricultural lime to raise pH')
    elif ph > 8.0:
        issues.append('High pH (Alkaline)')
        suggestions.append('Add sulfur or organic matter to lower pH')
    if moisture < 30:
        issues.append('Low moisture')
        suggestions.append('Implement irrigation or mulching')
    elif moisture > 80:
        issues.append('Excess moisture')
        suggestions.append('Improve drainage systems')
    if nitrogen < 30:
        issues.append('Low Nitrogen (N)')
        suggestions.append('Apply urea or ammonium nitrate fertilizer')
    if phosphorus < 30:
        issues.append('Low Phosphorus (P)')
        suggestions.append('Apply DAP or superphosphate fertilizer')
    if potassium < 30:
        issues.append('Low Potassium (K)')
        suggestions.append('Apply MOP (Muriate of Potash) fertilizer')

    return {
        'quality': quality,
        'ph_category': ph_category,
        'recommended_crops': recommended_crops,
        'issues': issues,
        'suggestions': suggestions,
        'score': _calculate_score(ph, moisture, nitrogen, phosphorus, potassium)
    }

def _rule_based_quality(ph, moisture, nitrogen, phosphorus, potassium):
    score = 0
    if 6.0 <= ph <= 7.5:
        score += 2
    elif 5.5 <= ph <= 8.0:
        score += 1
    if 40 <= moisture <= 70:
        score += 2
    elif 30 <= moisture <= 80:
        score += 1
    if nitrogen >= 50:
        score += 2
    elif nitrogen >= 30:
        score += 1
    if phosphorus >= 50:
        score += 2
    elif phosphorus >= 30:
        score += 1
    if potassium >= 50:
        score += 2
    elif potassium >= 30:
        score += 1

    if score >= 8:
        return 'Excellent'
    elif score >= 6:
        return 'Good'
    elif score >= 4:
        return 'Average'
    else:
        return 'Poor'

def _calculate_score(ph, moisture, nitrogen, phosphorus, potassium):
    score = 100
    if ph < 5.5 or ph > 8.5:
        score -= 20
    elif ph < 6.0 or ph > 8.0:
        score -= 10
    if moisture < 20 or moisture > 90:
        score -= 20
    elif moisture < 30 or moisture > 80:
        score -= 10
    for val in [nitrogen, phosphorus, potassium]:
        if val < 20:
            score -= 15
        elif val < 30:
            score -= 8
    return max(0, min(100, score))
