from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize database with the app"""
    db.init_app(app)
    with app.app_context():
        from database.models import (
            User, LandRecord, SoilAnalysis, CropDisease,
            PricePrediction, LandRegistry, LandAnalysis
        )
        db.create_all()
        _seed_land_registry()

def _seed_land_registry():
    """Seed 1000 land registry records if table is empty"""
    from database.models import LandRegistry
    if LandRegistry.query.count() > 0:
        return  # Already seeded

    import math
    STATES = ["Uttar Pradesh","Maharashtra","Punjab","Bihar","Rajasthan",
              "Madhya Pradesh","Gujarat","Haryana","Andhra Pradesh","Tamil Nadu",
              "Karnataka","Odisha","Telangana","Jharkhand","Chhattisgarh"]
    CITIES = {
        "Uttar Pradesh":  ["Lucknow","Agra","Varanasi","Kanpur","Allahabad","Meerut","Noida","Mathura","Firozabad","Jhansi","Gorakhpur"],
        "Maharashtra":    ["Mumbai","Pune","Nagpur","Nashik","Aurangabad","Solapur","Kolhapur","Amravati","Latur","Nanded"],
        "Punjab":         ["Amritsar","Ludhiana","Jalandhar","Patiala","Bathinda","Mohali","Ferozepur","Gurdaspur","Hoshiarpur","Moga"],
        "Bihar":          ["Patna","Gaya","Bhagalpur","Muzaffarpur","Darbhanga","Munger","Nalanda","Vaishali","Saran","Siwan"],
        "Rajasthan":      ["Jaipur","Jodhpur","Udaipur","Kota","Bikaner","Ajmer","Alwar","Bharatpur","Sikar","Tonk"],
        "Madhya Pradesh": ["Bhopal","Indore","Jabalpur","Gwalior","Ujjain","Sagar","Rewa","Satna","Ratlam","Dewas"],
        "Gujarat":        ["Ahmedabad","Surat","Vadodara","Rajkot","Bhavnagar","Jamnagar","Gandhinagar","Anand","Navsari","Junagadh"],
        "Haryana":        ["Gurugram","Faridabad","Ambala","Hisar","Karnal","Panipat","Rohtak","Sonipat","Yamunanagar","Panchkula"],
        "Andhra Pradesh": ["Visakhapatnam","Vijayawada","Guntur","Nellore","Kurnool","Kakinada","Tirupati","Kadapa","Anantapur","Eluru"],
        "Tamil Nadu":     ["Chennai","Coimbatore","Madurai","Tiruchirappalli","Salem","Tirunelveli","Erode","Vellore","Thoothukudi","Dindigul"],
        "Karnataka":      ["Bengaluru","Mysuru","Hubli","Mangaluru","Belagavi","Davangere","Ballari","Vijayapura","Shivamogga","Tumkur"],
        "Odisha":         ["Bhubaneswar","Cuttack","Rourkela","Berhampur","Sambalpur","Puri","Balasore","Baripada","Bhadrak","Jharsuguda"],
        "Telangana":      ["Hyderabad","Warangal","Nizamabad","Karimnagar","Khammam","Ramagundam","Mahbubnagar","Nalgonda","Adilabad","Suryapet"],
        "Jharkhand":      ["Ranchi","Jamshedpur","Dhanbad","Bokaro","Deoghar","Hazaribagh","Giridih","Ramgarh","Medininagar","Chaibasa"],
        "Chhattisgarh":   ["Raipur","Bhilai","Korba","Bilaspur","Durg","Rajnandgaon","Jagdalpur","Ambikapur","Chirmiri","Raigarh"],
    }
    OWNERS = ["Ramesh Kumar","Suresh Singh","Mohan Lal","Rajesh Yadav","Arun Kumar",
              "Vijay Prasad","Santosh Sharma","Dharam Singh","Hari Ram","Baldev Kumar",
              "Naresh Gupta","Prem Chand","Sita Devi","Lakshmi Bai","Sunita Devi",
              "Anita Kumari","Kavita Sharma","Meena Devi","Usha Rani","Rekha Devi",
              "Jagdish Prasad","Dinesh Kumar","Rakesh Verma","Mahesh Yadav","Ganesh Ram",
              "Shyam Lal","Radhe Shyam","Chandan Kumar","Manoj Singh","Ravi Shankar",
              "Govind Das","Bhola Nath","Nand Kumar","Sanjay Tiwari","Ashok Mishra",
              "Ramakant Dubey","Hemant Tripathi","Vinod Pandey","Sushil Kumar","Mukesh Sahu"]
    SOILS   = ["Alluvial Soil","Black Cotton Soil","Red Soil","Laterite Soil","Desert Soil","Loamy Soil","Sandy Soil","Clay Soil","Mountain Soil"]
    CROPS   = ["Wheat","Rice","Sugarcane","Cotton","Maize","Soybean","Pulses","Mustard","Groundnut","Potato","Onion","Tomato","Paddy","Barley","Jowar","Bajra"]
    WATER   = ["Canal","Borewell","River","Rainwater","Tube Well","Tank","Well","None"]
    LTYPES  = ["Agricultural","Residential","Commercial","Barren","Forest","Wetland"]
    STATUS  = ["Cultivated","Fallow","Under Development","Disputed","Clear Title","Mortgaged"]

    def sr(seed):
        x = math.sin(seed) * 10000
        return x - math.floor(x)

    records = []
    for i in range(1000):
        state  = STATES[int(sr(i*13+7)  * len(STATES))]
        cities = CITIES[state]
        city   = cities[int(sr(i*17+3)  * len(cities))]
        area   = round(0.5 + sr(i*23+11) * 15, 2)
        records.append(LandRegistry(
            khata_no      = f"KH-{int(sr(i*29+5)*9000)+1000:05d}",
            khesra_no     = f"KS-{int(sr(i*31+9)*9000)+1000:05d}",
            survey_no     = f"SV-{int(sr(i*37+13)*900)+100:04d}",
            owner_name    = OWNERS[int(sr(i*41+17) * len(OWNERS))],
            state         = state,
            city          = city,
            area          = area,
            soil_type     = SOILS[int(sr(i*43+19)  * len(SOILS))],
            land_type     = LTYPES[int(sr(i*47+23) * len(LTYPES))],
            crop_history  = ", ".join([CROPS[int(sr(i*13+7)*len(CROPS))], CROPS[int(sr(i*17+3)*len(CROPS))]]),
            water_source  = WATER[int(sr(i*53+29)  * len(WATER))],
            land_status   = STATUS[int(sr(i*59+31) * len(STATUS))],
            registered_year = 1990 + int(sr(i*61+37) * 34),
            ph_value      = round(5.5 + sr(i*67+41) * 3, 1),
        ))

    db.session.bulk_save_objects(records)
    db.session.commit()
    print(f"✅ Seeded 1000 land registry records")