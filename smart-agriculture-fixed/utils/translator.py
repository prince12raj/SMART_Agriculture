"""
Multi-language support utility.
Extend translations dict to add more languages and strings.
"""

TRANSLATIONS = {
    'en': {
        'welcome': 'Welcome',
        'dashboard': 'Dashboard',
        'land_records': 'Land Records',
        'soil_analysis': 'Soil Analysis',
        'disease_detection': 'Disease Detection',
        'price_prediction': 'Price Prediction',
        'grain_storage': 'Grain Storage',
        'logout': 'Logout',
        'submit': 'Submit',
        'analyze': 'Analyze',
        'predict': 'Predict',
        'add_record': 'Add Record',
        'result': 'Result',
        'recommended_crops': 'Recommended Crops',
        'suggestions': 'Suggestions',
    },
    'hi': {
        'welcome': 'स्वागत है',
        'dashboard': 'डैशबोर्ड',
        'land_records': 'भूमि रिकॉर्ड',
        'soil_analysis': 'मिट्टी विश्लेषण',
        'disease_detection': 'रोग पहचान',
        'price_prediction': 'मूल्य पूर्वानुमान',
        'grain_storage': 'अनाज भंडारण',
        'logout': 'लॉग आउट',
        'submit': 'जमा करें',
        'analyze': 'विश्लेषण करें',
        'predict': 'पूर्वानुमान करें',
        'add_record': 'रिकॉर्ड जोड़ें',
        'result': 'परिणाम',
        'recommended_crops': 'अनुशंसित फसलें',
        'suggestions': 'सुझाव',
    },
    'pa': {
        'welcome': 'ਜੀ ਆਇਆਂ ਨੂੰ',
        'dashboard': 'ਡੈਸ਼ਬੋਰਡ',
        'land_records': 'ਜ਼ਮੀਨ ਦੇ ਰਿਕਾਰਡ',
        'soil_analysis': 'ਮਿੱਟੀ ਵਿਸ਼ਲੇਸ਼ਣ',
        'disease_detection': 'ਰੋਗ ਪਛਾਣ',
        'price_prediction': 'ਕੀਮਤ ਅਨੁਮਾਨ',
        'grain_storage': 'ਅਨਾਜ ਭੰਡਾਰਣ',
        'logout': 'ਲੌਗ ਆਊਟ',
        'submit': 'ਜਮ੍ਹਾਂ ਕਰੋ',
        'analyze': 'ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ',
        'predict': 'ਅਨੁਮਾਨ ਲਗਾਓ',
        'add_record': 'ਰਿਕਾਰਡ ਜੋੜੋ',
        'result': 'ਨਤੀਜਾ',
        'recommended_crops': 'ਸਿਫਾਰਸ਼ੀ ਫਸਲਾਂ',
        'suggestions': 'ਸੁਝਾਅ',
    },
    'mr': {
        'welcome': 'स्वागत आहे',
        'dashboard': 'डॅशबोर्ड',
        'land_records': 'जमीन नोंदी',
        'soil_analysis': 'मातीचे विश्लेषण',
        'disease_detection': 'रोग ओळख',
        'price_prediction': 'किंमत अंदाज',
        'grain_storage': 'धान्य साठवण',
        'logout': 'बाहेर पडा',
        'submit': 'सबमिट करा',
        'analyze': 'विश्लेषण करा',
        'predict': 'अंदाज करा',
        'add_record': 'नोंद जोडा',
        'result': 'परिणाम',
        'recommended_crops': 'शिफारस केलेली पिके',
        'suggestions': 'सूचना',
    },
    'te': {
        'welcome': 'స్వాగతం',
        'dashboard': 'డాష్‌బోర్డ్',
        'land_records': 'భూమి రికార్డులు',
        'soil_analysis': 'మట్టి విశ్లేషణ',
        'disease_detection': 'వ్యాధి గుర్తింపు',
        'price_prediction': 'ధర అంచనా',
        'grain_storage': 'ధాన్యం నిల్వ',
        'logout': 'లాగ్అవుట్',
        'submit': 'సమర్పించు',
        'analyze': 'విశ్లేషించు',
        'predict': 'అంచనా వేయి',
        'add_record': 'రికార్డు జోడించు',
        'result': 'ఫలితం',
        'recommended_crops': 'సిఫారసు చేసిన పంటలు',
        'suggestions': 'సూచనలు',
    }
}

def translate(key, lang='en'):
    """Translate a key to the given language, fallback to English"""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    return lang_dict.get(key, TRANSLATIONS['en'].get(key, key))

def get_all_translations(lang='en'):
    """Get all translations for a given language"""
    base = TRANSLATIONS['en'].copy()
    base.update(TRANSLATIONS.get(lang, {}))
    return base

SUPPORTED_LANGUAGES = [
    {'code': 'en', 'name': 'English'},
    {'code': 'hi', 'name': 'हिंदी (Hindi)'},
    {'code': 'pa', 'name': 'ਪੰਜਾਬੀ (Punjabi)'},
    {'code': 'mr', 'name': 'मराठी (Marathi)'},
    {'code': 'te', 'name': 'తెలుగు (Telugu)'},
]
