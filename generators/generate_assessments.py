"""Generate RISK_ASSESSMENT, INSPECTION, HAZARD, and ACTION_ITEM tables."""
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
from config import (
    START_DATE, END_DATE, YEARS,
    RISK_ASSESSMENTS_PER_SCHOOL_PER_YEAR,
    INSPECTIONS_PER_SCHOOL_PER_YEAR_RANGE,
    INSPECTION_TYPES, INSPECTION_TYPE_WEIGHTS,
    COMPLIANCE_RATINGS, COMPLIANCE_WEIGHTS,
    HAZARD_TYPES, HAZARD_TYPE_WEIGHTS,
    HAZARD_CATEGORIES, HAZARD_CATEGORY_WEIGHTS,
    RISK_LEVELS, RISK_LEVEL_WEIGHTS,
    HAZARD_STATUSES,
    ACTION_PRIORITIES, ACTION_PRIORITY_WEIGHTS,
    ACTION_STATUSES,
    CONDITION_RATINGS,
)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')


def load_field_notes_templates():
    with open(os.path.join(TEMPLATES_DIR, 'field_notes_templates.json'), 'r') as f:
        return json.load(f)


def generate_findings_summary(templates, rng, site_name, num_hazards, num_actions, risk_level):
    """Generate a risk assessment findings summary."""
    template = rng.choice(templates['findings_templates'])
    concern = rng.choice(templates['concern_areas'])

    text = template
    text = text.replace('{site_name}', site_name)
    text = text.replace('{num_hazards}', str(num_hazards))
    text = text.replace('{num_actions}', str(num_actions))
    text = text.replace('{risk_level}', risk_level.lower())
    text = text.replace('{concern_area}', concern)
    text = text.replace('{action_area}', rng.choice(templates['concern_areas']))
    text = text.replace('{timeframe}', rng.choice(['30 days', '60 days', '14 days', 'the next term']))
    text = text.replace('{existing}', str(rng.integers(1, 8)))
    text = text.replace('{finding1}', rng.choice(templates['observations']))
    text = text.replace('{finding2}', rng.choice(templates['observations']))
    text = text.replace('{area}', rng.choice(['the main block', 'outdoor areas', 'the sports facilities', 'administration building']))
    text = text.replace('{emergency_status}', rng.choice(['adequate', 'requiring update', 'satisfactory']))
    text = text.replace('{num_buildings}', str(rng.integers(3, 12)))
    text = text.replace('{improvement_area}', rng.choice(templates['improvements']))
    text = text.replace('{date}', 'the assessment date')
    text = text.replace('{critical_count}', str(rng.integers(0, 3)))
    return text


def generate_field_notes(templates, rng, site_name, contractor_name=None):
    """Generate inspection field notes."""
    template = rng.choice(templates['field_notes_templates'])

    text = template
    text = text.replace('{site_name}', site_name)
    text = text.replace('{time}', f"{rng.integers(8,16)}:{rng.choice(['00','15','30','45'])}")
    text = text.replace('{role}', rng.choice(['the site manager', 'the principal', 'the caretaker', 'the H&S rep']))
    text = text.replace('{report}', rng.choice(['no issues since last visit', 'a concern about the car park', 'a recent near-miss in the workshop', 'ongoing roof leak in Block B']))
    text = text.replace('{start_area}', rng.choice(['the main entrance', 'the car park', 'Block A', 'the playground']))
    text = text.replace('{observation1}', rng.choice(templates['observations']))
    text = text.replace('{observation2}', rng.choice(templates['observations']))
    text = text.replace('{building}', rng.choice(['Block A', 'the gymnasium', 'the library', 'the hall']))
    text = text.replace('{condition}', rng.choice(['in good condition', 'showing signs of wear', 'in need of maintenance', 'satisfactory']))
    text = text.replace('{recommendation}', rng.choice(['scheduling maintenance within 30 days', 'immediate action on high-risk items', 'review at next assessment', 'engaging specialist contractor']))
    text = text.replace('{status}', rng.choice(['cordoned off', 'cleaned up', 'under repair', 'unchanged']))
    text = text.replace('{confirmation}', rng.choice(['the timeline of events', 'that protocols were followed', 'that the issue has been ongoing', 'awareness of the hazard']))
    text = text.replace('{root_cause}', rng.choice(['worn equipment', 'lack of maintenance', 'environmental conditions', 'inadequate training']))
    text = text.replace('{controls}', rng.choice(['area barricaded', 'equipment isolated', 'warning signs placed', 'temporary repair applied']))
    text = text.replace('{further}', rng.choice(['yes - engineering assessment required', 'no - matter resolved', 'yes - WorkSafe notification pending', 'yes - await contractor quote']))
    text = text.replace('{contractor}', contractor_name or 'the contractor')
    text = text.replace('{work_type}', rng.choice(['roof repairs', 'electrical maintenance', 'plumbing work', 'grounds maintenance', 'painting', 'HVAC servicing']))
    text = text.replace('{ppe_status}', rng.choice(templates['ppe_statuses']))
    text = text.replace('{induction_status}', rng.choice(['current', 'expired - updated on site', 'missing for one worker', 'all current']))
    text = text.replace('{method_status}', rng.choice(['provided and adequate', 'generic - not site-specific', 'not available', 'comprehensive']))
    text = text.replace('{compliance_rating}', rng.choice(['compliant', 'minor non-compliance', 'major non-compliance']))
    text = text.replace('{issues}', rng.choice(['none noted', 'PPE not consistently worn', 'work area not adequately fenced', 'SWMS not signed', 'no issues']))
    text = text.replace('{complaint}', rng.choice(templates['complaints']))
    text = text.replace('{finding}', rng.choice(templates['observations']))
    text = text.replace('{response}', rng.choice(['aware of the issue', 'unaware until now', 'already arranging repair', 'concerned about the situation']))
    text = text.replace('{actions}', rng.choice(['repair ordered', 'contractor engaged', 'temporary fix applied', 'area isolated']))
    text = text.replace('{followup}', rng.choice(['yes - in 14 days', 'no', 'yes - after repair completed', 'yes - next routine visit']))
    text = text.replace('{exit_status}', rng.choice(['clear', 'one partially blocked', 'all clear', 'signage missing on one']))
    text = text.replace('{fire_status}', rng.choice(['all in date', 'two expired', 'all current', 'one missing from hall']))
    text = text.replace('{firstaid_status}', rng.choice(['fully stocked', 'low on supplies', 'adequate', 'needs restocking']))
    text = text.replace('{signage_status}', rng.choice(['adequate', 'faded in places', 'good', 'several missing']))
    text = text.replace('{housekeeping}', rng.choice(['good', 'satisfactory', 'poor in storage areas', 'excellent']))
    text = text.replace('{num_hazards}', str(rng.integers(0, 5)))
    return text


def generate_hazard_description(rng, hazard_type, hazard_category, building_name=None, asset_name=None):
    """Generate a hazard description."""
    location = building_name or rng.choice(['the northern boundary', 'the main entrance', 'the sports field perimeter', 'near the car park', 'adjacent to the playground'])

    descriptions = {
        'SLIP_TRIP_FALL': [f"Uneven paving stones near {location} creating trip hazard", f"Algae growth on pathway near {location} making surface slippery in wet conditions", f"Worn carpet edge in {location} creating trip point"],
        'FALLING_OBJECTS': [f"Loose guttering on {location} at risk of falling in high winds", f"Unsecured items stored at height in {location}", f"Deteriorating fascia boards above {location} walkway"],
        'MACHINERY': [f"Missing guard on equipment in {location}", f"Worn blade on grounds equipment stored in {location}", f"Inadequate lockout procedure for machinery in {location}"],
        'TRAFFIC': ["Inadequate separation between pedestrians and vehicles in drop-off zone", "Poor visibility at car park exit due to vegetation", "No speed limit signage in school grounds"],
        'WEATHER': [f"Ponding water near {location} after rainfall", "Ice formation on north-facing pathways in winter", f"Wind exposure to portable buildings near {location}"],
        'ASBESTOS': [f"Suspected ACM in ceiling tiles of {location} (pre-1990 construction)", f"Damaged soffit near {location} potentially containing asbestos", "Asbestos register requires update for recent renovations"],
        'WATER': ["Stormwater drain cover missing near playground", f"Flooding risk to {location} from blocked drain", "Standing water creating mosquito breeding ground"],
        'TREES': [f"Dead branch overhanging walkway near {location}", "Large tree root lifting pathway surface", f"Unstable tree identified near {location} boundary"],
        'PLAYGROUND': ["Worn impact-absorbing surface below climbing frame", "Rusted bolt on swing frame", "Gap in playground fencing allowing access to road"],
        'ELECTRICAL': [f"Damaged power point cover in {location}", "Overhead power lines within reach of tree growth", f"Worn cable on portable equipment in {location}"],
        'HEIGHTS': [f"No edge protection on {location} roof access", "Inadequate ladder storage and inspection regime", f"Unprotected mezzanine edge in {location}"],
    }

    options = descriptions.get(hazard_category, [f"General hazard identified at {location}"])
    return rng.choice(options)


def generate_all(sites_df, buildings_df, assets_df, people_df, contractors_df, site_contractors_df, seed=48):
    """Generate risk assessments, inspections, hazards, and action items."""
    rng = np.random.default_rng(seed)
    templates = load_field_notes_templates()

    # Pre-index
    people_by_site = people_df.groupby('site_id')['person_id'].apply(list).to_dict()
    buildings_by_site = buildings_df.groupby('site_id', group_keys=False).apply(lambda x: x[['building_id', 'building_name']].to_dict('records'), include_groups=False).to_dict()
    assets_by_site = assets_df.groupby('site_id', group_keys=False).apply(lambda x: x[['asset_id', 'asset_name']].to_dict('records'), include_groups=False).to_dict()
    sc_by_site = site_contractors_df.groupby('site_id')['contractor_id'].apply(list).to_dict()
    contractor_names = contractors_df.set_index('contractor_id')['company_name'].to_dict()

    assessments = []
    inspections = []
    hazards = []
    actions = []

    assessment_id = 1
    inspection_id = 1
    hazard_id = 1
    action_id = 1

    total_sites = len(sites_df)

    for idx, (_, site) in enumerate(sites_df.iterrows()):
        if idx % 500 == 0:
            print(f"  Processing site {idx}/{total_sites}...")

        site_id = site['site_id']
        site_name = site['site_name']
        site_people = people_by_site.get(site_id, [])
        site_buildings = buildings_by_site.get(site_id, [])
        site_assets = assets_by_site.get(site_id, [])
        site_contractor_ids = sc_by_site.get(site_id, [])

        if not site_people:
            continue

        # --- RISK ASSESSMENTS (2 per year) ---
        for year in YEARS:
            for half in range(2):
                if year == 2025 and half == 1:
                    continue  # H2 2025 not yet done

                period = f"H{half+1}_{year}"
                month = 3 + half * 6  # H1=March, H2=September
                day = int(rng.integers(1, 28))
                assessment_date = datetime(year, month, day)

                num_hazards_found = int(rng.integers(0, 5))
                num_actions_created = int(rng.integers(0, num_hazards_found + 2))
                risk_score = int(rng.integers(10, 90))
                risk_level = 'LOW' if risk_score < 30 else 'MEDIUM' if risk_score < 60 else 'HIGH' if risk_score < 80 else 'CRITICAL'

                findings = generate_findings_summary(templates, rng, site_name, num_hazards_found, num_actions_created, risk_level)
                conductor = int(rng.choice(site_people))

                assessments.append({
                    'assessment_id': assessment_id,
                    'site_id': site_id,
                    'conducted_by_person_id': conductor,
                    'assessment_date': assessment_date.strftime('%Y-%m-%d'),
                    'assessment_period': period,
                    'overall_risk_score': risk_score,
                    'findings_summary': findings,
                    'num_hazards_identified': num_hazards_found,
                    'num_actions_created': num_actions_created,
                    'status': 'COMPLETED' if year < 2025 else rng.choice(['COMPLETED', 'REVIEWED']),
                })

                # Create hazards from this assessment
                for _ in range(num_hazards_found):
                    h_type = rng.choice(HAZARD_TYPES, p=HAZARD_TYPE_WEIGHTS)
                    h_cat = rng.choice(HAZARD_CATEGORIES, p=HAZARD_CATEGORY_WEIGHTS)
                    h_risk = rng.choice(RISK_LEVELS, p=RISK_LEVEL_WEIGHTS)

                    # 40% linked to building, 15% to asset, 45% environmental
                    h_building_id = None
                    h_building_name = None
                    h_asset_id = None
                    r = rng.random()
                    if r < 0.4 and site_buildings:
                        bldg = site_buildings[int(rng.integers(0, len(site_buildings)))]
                        h_building_id = bldg['building_id']
                        h_building_name = bldg['building_name']
                    elif r < 0.55 and site_assets:
                        asset = site_assets[int(rng.integers(0, len(site_assets)))]
                        h_asset_id = asset['asset_id']

                    desc = generate_hazard_description(rng, h_type, h_cat, h_building_name)

                    # Older hazards more likely controlled/eliminated
                    days_ago = (datetime(2025, 6, 30) - assessment_date).days
                    if days_ago > 365:
                        h_status = rng.choice(HAZARD_STATUSES, p=[0.15, 0.40, 0.30, 0.15])
                    else:
                        h_status = rng.choice(HAZARD_STATUSES, p=[0.40, 0.30, 0.10, 0.20])

                    hazards.append({
                        'hazard_id': hazard_id,
                        'site_id': site_id,
                        'building_id': h_building_id,
                        'asset_id': h_asset_id,
                        'hazard_type': h_type,
                        'hazard_category': h_cat,
                        'description': desc,
                        'location_description': h_building_name or 'School grounds',
                        'risk_level': h_risk,
                        'status': h_status,
                        'identified_date': assessment_date.strftime('%Y-%m-%d'),
                        'identified_by_assessment_id': assessment_id,
                        'identified_by_inspection_id': None,
                        'control_measures': None if h_status == 'OPEN' else 'Controls applied as per action plan',
                    })
                    hazard_id += 1

                # Create actions from this assessment
                for _ in range(num_actions_created):
                    priority = rng.choice(ACTION_PRIORITIES, p=ACTION_PRIORITY_WEIGHTS)
                    due_days = {'LOW': 90, 'MEDIUM': 60, 'HIGH': 30, 'CRITICAL': 14}[priority]
                    due_date = assessment_date + timedelta(days=due_days + int(rng.integers(-7, 7)))
                    created_date = assessment_date

                    # Determine status based on current date vs due date
                    if due_date < datetime(2025, 6, 30):
                        if rng.random() < 0.7:
                            status = 'COMPLETED'
                            completed_date = due_date - timedelta(days=int(rng.integers(0, due_days // 2)))
                        elif rng.random() < 0.5:
                            status = 'OVERDUE'
                            completed_date = None
                        else:
                            status = 'IN_PROGRESS'
                            completed_date = None
                    else:
                        status = rng.choice(['OPEN', 'IN_PROGRESS'])
                        completed_date = None

                    actions.append({
                        'action_id': action_id,
                        'site_id': site_id,
                        'hazard_id': hazards[-1]['hazard_id'] if hazards and hazards[-1]['site_id'] == site_id else None,
                        'assessment_id': assessment_id,
                        'inspection_id': None,
                        'assigned_to_person_id': int(rng.choice(site_people)),
                        'action_description': rng.choice([
                            'Repair or replace damaged infrastructure',
                            'Install additional safety signage',
                            'Engage contractor for specialist repair',
                            'Conduct staff training on updated procedure',
                            'Apply anti-slip treatment to surface',
                            'Remove or trim vegetation creating hazard',
                            'Install guard rail or barrier',
                            'Update emergency procedures documentation',
                            'Schedule professional inspection',
                            'Replace worn equipment',
                            'Improve lighting in affected area',
                            'Review and update risk register',
                        ]),
                        'priority': priority,
                        'due_date': due_date.strftime('%Y-%m-%d'),
                        'completed_date': completed_date.strftime('%Y-%m-%d') if completed_date else None,
                        'status': status,
                        'created_date': created_date.strftime('%Y-%m-%d'),
                        'notes': None,
                    })
                    action_id += 1

                assessment_id += 1

        # --- INSPECTIONS (ad-hoc, 1-4 per year) ---
        for year in YEARS:
            num_inspections = int(rng.integers(*INSPECTIONS_PER_SCHOOL_PER_YEAR_RANGE))
            if year == 2025:
                num_inspections = num_inspections // 2

            for _ in range(num_inspections):
                month = int(rng.integers(2, 12))
                day = int(rng.integers(1, 28))
                insp_date = datetime(year, month, day)

                insp_type = rng.choice(INSPECTION_TYPES, p=INSPECTION_TYPE_WEIGHTS)
                compliance = rng.choice(COMPLIANCE_RATINGS, p=COMPLIANCE_WEIGHTS)

                # Contractor audit links to a contractor
                insp_contractor_id = None
                contractor_name = None
                if insp_type == 'CONTRACTOR_AUDIT' and site_contractor_ids:
                    insp_contractor_id = int(rng.choice(site_contractor_ids))
                    contractor_name = contractor_names.get(insp_contractor_id)

                num_hazards_found = int(rng.integers(0, 4))
                num_actions_created = int(rng.integers(0, num_hazards_found + 1))

                field_notes = generate_field_notes(templates, rng, site_name, contractor_name)
                conductor = int(rng.choice(site_people))

                inspections.append({
                    'inspection_id': inspection_id,
                    'site_id': site_id,
                    'conducted_by_person_id': conductor,
                    'contractor_id': insp_contractor_id,
                    'inspection_date': insp_date.strftime('%Y-%m-%d'),
                    'inspection_type': insp_type,
                    'field_notes': field_notes,
                    'compliance_rating': compliance,
                    'num_hazards_identified': num_hazards_found,
                    'num_actions_created': num_actions_created,
                    'status': 'COMPLETED',
                })

                # Create hazards from inspection
                for _ in range(num_hazards_found):
                    h_type = rng.choice(HAZARD_TYPES, p=HAZARD_TYPE_WEIGHTS)
                    h_cat = rng.choice(HAZARD_CATEGORIES, p=HAZARD_CATEGORY_WEIGHTS)
                    h_risk = rng.choice(RISK_LEVELS, p=RISK_LEVEL_WEIGHTS)

                    h_building_id = None
                    h_building_name = None
                    h_asset_id = None
                    r = rng.random()
                    if r < 0.4 and site_buildings:
                        bldg = site_buildings[int(rng.integers(0, len(site_buildings)))]
                        h_building_id = bldg['building_id']
                        h_building_name = bldg['building_name']
                    elif r < 0.55 and site_assets:
                        asset = site_assets[int(rng.integers(0, len(site_assets)))]
                        h_asset_id = asset['asset_id']

                    desc = generate_hazard_description(rng, h_type, h_cat, h_building_name)
                    days_ago = (datetime(2025, 6, 30) - insp_date).days
                    if days_ago > 365:
                        h_status = rng.choice(HAZARD_STATUSES, p=[0.15, 0.40, 0.30, 0.15])
                    else:
                        h_status = rng.choice(HAZARD_STATUSES, p=[0.40, 0.30, 0.10, 0.20])

                    hazards.append({
                        'hazard_id': hazard_id,
                        'site_id': site_id,
                        'building_id': h_building_id,
                        'asset_id': h_asset_id,
                        'hazard_type': h_type,
                        'hazard_category': h_cat,
                        'description': desc,
                        'location_description': h_building_name or 'School grounds',
                        'risk_level': h_risk,
                        'status': h_status,
                        'identified_date': insp_date.strftime('%Y-%m-%d'),
                        'identified_by_assessment_id': None,
                        'identified_by_inspection_id': inspection_id,
                        'control_measures': None if h_status == 'OPEN' else 'Controls applied as per action plan',
                    })
                    hazard_id += 1

                # Create actions from inspection
                for _ in range(num_actions_created):
                    priority = rng.choice(ACTION_PRIORITIES, p=ACTION_PRIORITY_WEIGHTS)
                    due_days = {'LOW': 90, 'MEDIUM': 60, 'HIGH': 30, 'CRITICAL': 14}[priority]
                    due_date = insp_date + timedelta(days=due_days + int(rng.integers(-7, 7)))
                    created_date = insp_date

                    if due_date < datetime(2025, 6, 30):
                        if rng.random() < 0.7:
                            status = 'COMPLETED'
                            completed_date = due_date - timedelta(days=int(rng.integers(0, due_days // 2)))
                        elif rng.random() < 0.5:
                            status = 'OVERDUE'
                            completed_date = None
                        else:
                            status = 'IN_PROGRESS'
                            completed_date = None
                    else:
                        status = rng.choice(['OPEN', 'IN_PROGRESS'])
                        completed_date = None

                    actions.append({
                        'action_id': action_id,
                        'site_id': site_id,
                        'hazard_id': hazards[-1]['hazard_id'] if hazards and hazards[-1]['site_id'] == site_id else None,
                        'assessment_id': None,
                        'inspection_id': inspection_id,
                        'assigned_to_person_id': int(rng.choice(site_people)),
                        'action_description': rng.choice([
                            'Repair or replace damaged infrastructure',
                            'Install additional safety signage',
                            'Engage contractor for specialist repair',
                            'Conduct staff training on updated procedure',
                            'Apply anti-slip treatment to surface',
                            'Remove or trim vegetation creating hazard',
                            'Install guard rail or barrier',
                            'Update emergency procedures documentation',
                            'Schedule professional inspection',
                            'Replace worn equipment',
                            'Improve lighting in affected area',
                            'Review and update risk register',
                        ]),
                        'priority': priority,
                        'due_date': due_date.strftime('%Y-%m-%d'),
                        'completed_date': completed_date.strftime('%Y-%m-%d') if completed_date else None,
                        'status': status,
                        'created_date': created_date.strftime('%Y-%m-%d'),
                        'notes': None,
                    })
                    action_id += 1

                inspection_id += 1

    return (
        pd.DataFrame(assessments),
        pd.DataFrame(inspections),
        pd.DataFrame(hazards),
        pd.DataFrame(actions),
    )


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Loading source data...")
    sites = pd.read_csv(os.path.join(OUTPUT_DIR, 'site.csv'))
    buildings = pd.read_csv(os.path.join(OUTPUT_DIR, 'building.csv'))
    assets = pd.read_csv(os.path.join(OUTPUT_DIR, 'asset.csv'))
    people = pd.read_csv(os.path.join(OUTPUT_DIR, 'person.csv'))
    contractors = pd.read_csv(os.path.join(OUTPUT_DIR, 'contractor.csv'))
    site_contractors = pd.read_csv(os.path.join(OUTPUT_DIR, 'site_contractor.csv'))

    print("Generating risk assessments, inspections, hazards, actions...")
    assessments_df, inspections_df, hazards_df, actions_df = generate_all(
        sites, buildings, assets, people, contractors, site_contractors
    )

    assessments_df.to_csv(os.path.join(OUTPUT_DIR, 'risk_assessment.csv'), index=False)
    print(f"Generated {len(assessments_df)} risk assessments")

    inspections_df.to_csv(os.path.join(OUTPUT_DIR, 'inspection.csv'), index=False)
    print(f"Generated {len(inspections_df)} inspections")

    hazards_df.to_csv(os.path.join(OUTPUT_DIR, 'hazard.csv'), index=False)
    print(f"Generated {len(hazards_df)} hazards")

    actions_df.to_csv(os.path.join(OUTPUT_DIR, 'action_item.csv'), index=False)
    print(f"Generated {len(actions_df)} action items")
