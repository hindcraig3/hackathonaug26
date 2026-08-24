"""Central configuration for the H&S workshop data generators."""
from datetime import date

# Date range
START_DATE = date(2020, 1, 1)
END_DATE = date(2025, 6, 30)
YEARS = list(range(2020, 2026))

# NZ school terms (approximate)
TERM_DATES = [
    (2, 4),   # Term 1: Feb - Apr
    (5, 7),   # Term 2: May - Jul
    (7, 9),   # Term 3: Jul - Sep
    (10, 12), # Term 4: Oct - Dec
]
HOLIDAY_MONTHS = [1, 12]  # Jan and late Dec

# Volume controls
INCIDENTS_PER_SCHOOL_PER_YEAR_RANGE = (5, 15)
RISK_ASSESSMENTS_PER_SCHOOL_PER_YEAR = 2
INSPECTIONS_PER_SCHOOL_PER_YEAR_RANGE = (1, 4)
NUM_CONTRACTORS = 150

# Building assignment by school size
BUILDING_CONFIG = {
    'large': {'min': 8, 'max': 12, 'roll_threshold': 500},
    'medium': {'min': 5, 'max': 8, 'roll_threshold': 200},
    'small': {'min': 3, 'max': 5, 'roll_threshold': 0},
}

ASSET_CONFIG = {
    'large': {'min': 20, 'max': 30},
    'medium': {'min': 12, 'max': 20},
    'small': {'min': 8, 'max': 12},
}

# Lookup values
BUILDING_TYPES = [
    'CLASSROOM', 'GYM', 'LIBRARY', 'ADMIN', 'HALL',
    'WORKSHOP', 'STORAGE', 'TOILET_BLOCK', 'SPORTS_PAVILION'
]

BUILDING_NAMES = {
    'CLASSROOM': ['Block A', 'Block B', 'Block C', 'Block D', 'Block E', 'Junior Block', 'Senior Block', 'Science Block', 'Technology Block', 'Arts Block'],
    'GYM': ['Main Gymnasium', 'Sports Hall', 'Fitness Centre'],
    'LIBRARY': ['School Library', 'Learning Centre', 'Resource Centre'],
    'ADMIN': ['Administration Building', 'Main Office', 'Staff Block'],
    'HALL': ['Assembly Hall', 'School Hall', 'Performing Arts Centre'],
    'WORKSHOP': ['Technology Workshop', 'Metal Workshop', 'Wood Workshop', 'Food Technology'],
    'STORAGE': ['Equipment Store', 'Grounds Shed', 'Sports Store', 'Maintenance Shed'],
    'TOILET_BLOCK': ['Junior Toilets', 'Senior Toilets', 'Staff Facilities', 'Sports Amenities'],
    'SPORTS_PAVILION': ['Cricket Pavilion', 'Sports Pavilion', 'Changing Rooms'],
}

ASSET_TYPES = [
    'HVAC', 'ELECTRICAL', 'PLAYGROUND', 'VEHICLE', 'GROUNDS_EQUIPMENT',
    'MACHINERY', 'CAR_PARK', 'BUS_STOP', 'SPORTS_EQUIPMENT', 'FENCING', 'ROOFING'
]

ASSET_NAMES = {
    'HVAC': ['Heat Pump Unit', 'Central Heating System', 'Air Conditioning Unit', 'Ventilation System', 'Boiler'],
    'ELECTRICAL': ['Main Switchboard', 'Solar Panel Array', 'Emergency Lighting', 'Generator', 'EV Charger'],
    'PLAYGROUND': ['Junior Playground', 'Senior Playground', 'Adventure Playground', 'Swing Set', 'Climbing Frame', 'Flying Fox'],
    'VEHICLE': ['School Van', 'Ride-on Mower', 'Utility Vehicle', 'School Bus'],
    'GROUNDS_EQUIPMENT': ['Lawn Mower', 'Line Marker', 'Leaf Blower', 'Chainsaw', 'Hedge Trimmer', 'Pressure Washer'],
    'MACHINERY': ['Workshop Lathe', 'Drill Press', 'Band Saw', 'Table Saw', 'CNC Router', '3D Printer'],
    'CAR_PARK': ['Staff Car Park', 'Visitor Car Park', 'Drop-off Zone', 'Bus Bay'],
    'BUS_STOP': ['Main Bus Stop', 'Secondary Bus Stop', 'Kiss and Ride Zone'],
    'SPORTS_EQUIPMENT': ['Basketball Hoops', 'Netball Courts', 'Tennis Court', 'Swimming Pool', 'Cricket Nets', 'Long Jump Pit'],
    'FENCING': ['Perimeter Fence - North', 'Perimeter Fence - South', 'Pool Fence', 'Sports Field Fence'],
    'ROOFING': ['Main Block Roof', 'Hall Roof', 'Gym Roof', 'Library Roof'],
}

CONDITION_RATINGS = ['GOOD', 'FAIR', 'POOR', 'CRITICAL']
CONDITION_WEIGHTS = [0.4, 0.35, 0.2, 0.05]

PERSON_ROLES = ['PRINCIPAL', 'SITE_MANAGER', 'HS_REP', 'CARETAKER']

CONTRACTOR_SERVICE_TYPES = [
    'BUILDING_MAINTENANCE', 'ELECTRICAL', 'PLUMBING', 'CLEANING',
    'GROUNDS', 'IT_SERVICES', 'PAINTING', 'ROOFING', 'SECURITY', 'HVAC'
]

CONTRACTOR_NAME_PREFIXES = [
    'Pacific', 'Southern', 'Kiwi', 'Aotearoa', 'Peninsula', 'Coastal',
    'Alpine', 'Metro', 'Regional', 'Premier', 'Elite', 'Reliable',
    'Precision', 'Summit', 'Horizon', 'Sterling', 'Pinnacle', 'Apex'
]

CONTRACTOR_NAME_SUFFIXES = [
    'Services Ltd', 'Solutions NZ', 'Group', 'Contractors', 'Enterprises',
    'Holdings', 'Technical Services', 'Maintenance Co', 'Property Services', 'Works'
]

NZ_REGIONS = [
    'Northland Region', 'Auckland Region', 'Waikato Region', 'Bay of Plenty Region',
    'Gisborne Region', 'Hawke\'s Bay Region', 'Taranaki Region', 'Manawatū-Whanganui Region',
    'Wellington Region', 'Tasman Region', 'Nelson Region', 'Marlborough Region',
    'West Coast Region', 'Canterbury Region', 'Otago Region', 'Southland Region'
]

# Incident configuration
INCIDENT_TYPES = ['INJURY', 'NEAR_MISS', 'PROPERTY_DAMAGE', 'ENVIRONMENTAL', 'SECURITY']
INCIDENT_TYPE_WEIGHTS = [0.35, 0.35, 0.15, 0.10, 0.05]

SEVERITY_LEVELS = ['MINOR', 'MODERATE', 'SERIOUS_HARM', 'NOTIFIABLE']
SEVERITY_WEIGHTS = [0.50, 0.30, 0.15, 0.05]

BODY_PARTS = ['HEAD', 'BACK', 'HAND', 'LEG', 'FOOT', 'ARM', 'SHOULDER', 'KNEE', 'MULTIPLE', 'NA']
BODY_PART_WEIGHTS = [0.08, 0.15, 0.15, 0.12, 0.10, 0.12, 0.08, 0.08, 0.05, 0.07]

ACTIVITIES = ['TEACHING', 'MAINTENANCE', 'SPORT', 'TRANSIT', 'CLEANING', 'CONSTRUCTION', 'PLAY', 'ADMIN']
ACTIVITY_WEIGHTS = [0.15, 0.20, 0.15, 0.10, 0.10, 0.10, 0.15, 0.05]

LOCATION_TYPES = ['INDOOR', 'OUTDOOR', 'CARPARK', 'PLAYGROUND', 'SPORTS_FIELD', 'STAIRWELL', 'WORKSHOP', 'KITCHEN']
LOCATION_TYPE_WEIGHTS = [0.25, 0.20, 0.08, 0.15, 0.10, 0.10, 0.07, 0.05]

ROOT_CAUSES = ['HUMAN_ERROR', 'EQUIPMENT_FAILURE', 'ENVIRONMENTAL', 'PROCEDURAL', 'TRAINING_GAP']
ROOT_CAUSE_WEIGHTS = [0.30, 0.20, 0.20, 0.20, 0.10]

INVESTIGATION_STATUSES = ['OPEN', 'IN_PROGRESS', 'CLOSED']

# Hazard configuration
HAZARD_TYPES = ['PHYSICAL', 'CHEMICAL', 'BIOLOGICAL', 'ERGONOMIC', 'ENVIRONMENTAL', 'ELECTRICAL', 'STRUCTURAL']
HAZARD_TYPE_WEIGHTS = [0.30, 0.05, 0.05, 0.10, 0.25, 0.10, 0.15]

HAZARD_CATEGORIES = [
    'SLIP_TRIP_FALL', 'FALLING_OBJECTS', 'MACHINERY', 'TRAFFIC',
    'WEATHER', 'ASBESTOS', 'WATER', 'TREES', 'PLAYGROUND', 'ELECTRICAL', 'HEIGHTS'
]
HAZARD_CATEGORY_WEIGHTS = [0.20, 0.08, 0.08, 0.10, 0.08, 0.05, 0.08, 0.10, 0.08, 0.08, 0.07]

RISK_LEVELS = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
RISK_LEVEL_WEIGHTS = [0.25, 0.40, 0.25, 0.10]

HAZARD_STATUSES = ['OPEN', 'CONTROLLED', 'ELIMINATED', 'MONITORING']

# Inspection configuration
INSPECTION_TYPES = ['ROUTINE', 'POST_INCIDENT', 'CONTRACTOR_AUDIT', 'COMPLAINT_RESPONSE']
INSPECTION_TYPE_WEIGHTS = [0.40, 0.25, 0.25, 0.10]

COMPLIANCE_RATINGS = ['COMPLIANT', 'MINOR_NON_COMPLIANCE', 'MAJOR_NON_COMPLIANCE', 'CRITICAL']
COMPLIANCE_WEIGHTS = [0.45, 0.30, 0.20, 0.05]

# Action item configuration
ACTION_PRIORITIES = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
ACTION_PRIORITY_WEIGHTS = [0.20, 0.40, 0.30, 0.10]

ACTION_STATUSES = ['OPEN', 'IN_PROGRESS', 'OVERDUE', 'COMPLETED', 'CANCELLED']

SAFETY_RATINGS = ['A', 'B', 'C', 'D']
SAFETY_RATING_WEIGHTS = [0.30, 0.40, 0.20, 0.10]
