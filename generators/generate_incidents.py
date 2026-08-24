"""Generate INCIDENT table with hybrid narratives."""
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
from config import (
    START_DATE, END_DATE, YEARS, HOLIDAY_MONTHS,
    INCIDENTS_PER_SCHOOL_PER_YEAR_RANGE,
    INCIDENT_TYPES, INCIDENT_TYPE_WEIGHTS,
    SEVERITY_LEVELS, SEVERITY_WEIGHTS,
    BODY_PARTS, BODY_PART_WEIGHTS,
    ACTIVITIES, ACTIVITY_WEIGHTS,
    LOCATION_TYPES, LOCATION_TYPE_WEIGHTS,
    ROOT_CAUSES, ROOT_CAUSE_WEIGHTS,
    INVESTIGATION_STATUSES,
)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')


def load_narrative_templates():
    with open(os.path.join(TEMPLATES_DIR, 'incident_narratives.json'), 'r') as f:
        return json.load(f)


def generate_realistic_narrative(template_data, rng, site, building_name, contractor_name, body_part, date_str):
    """Pick a realistic narrative template and fill in variables."""
    narratives = template_data['realistic_narratives']
    chosen = narratives[int(rng.integers(0, len(narratives)))]

    text = chosen['template']
    text = text.replace('{site_name}', site['site_name'])
    text = text.replace('{building}', building_name or 'the main block')
    text = text.replace('{contractor}', contractor_name or 'the maintenance contractor')
    text = text.replace('{body_part}', body_part.lower().replace('_', ' '))
    text = text.replace('{date}', date_str)
    text = text.replace('{role}', rng.choice(['a staff member', 'the caretaker', 'a teacher', 'the site manager']))

    return text, chosen.get('type'), chosen.get('severity'), chosen.get('location_type'), chosen.get('activity'), chosen.get('root_cause')


def generate_template_narrative(template_data, rng, body_part):
    """Generate a narrative from template patterns."""
    patterns = template_data['template_patterns']
    components = template_data['template_components']

    pattern = rng.choice(patterns)
    text = pattern
    text = text.replace('{role}', rng.choice(components['roles']))
    text = text.replace('{action}', rng.choice(components['actions']))
    text = text.replace('{activity_desc}', rng.choice(components['activity_descs']))
    text = text.replace('{event}', rng.choice(components['events']))
    text = text.replace('{outcome}', rng.choice(components['outcomes']))
    text = text.replace('{follow_up}', rng.choice(components['follow_ups']))
    text = text.replace('{injury_desc}', rng.choice(components['outcomes']))
    text = text.replace('{action_taken}', rng.choice(components['follow_ups']))
    text = text.replace('{body_part}', body_part.lower().replace('_', ' '))
    text = text.replace('{location}', rng.choice(['the hallway', 'the stairwell', 'the car park', 'the playground', 'the sports field', 'the workshop', 'the classroom']))
    text = text.replace('{time}', f"{rng.integers(7,17)}:{rng.choice(['00','15','30','45'])}{'am' if rng.integers(7,17) < 12 else 'pm'}")
    text = text.replace('{date}', 'the reported date')

    return text


def generate_incident_date(rng, year):
    """Generate a date weighted toward term time."""
    # Avoid Jan and late Dec (holidays)
    month = int(rng.choice([2,3,4,5,6,7,8,9,10,11], p=[0.10,0.12,0.10,0.10,0.08,0.08,0.08,0.10,0.12,0.12]))
    day = int(rng.integers(1, 29))
    hour = int(rng.integers(7, 17))
    minute = int(rng.integers(0, 60))
    return datetime(year, month, day, hour, minute)


def generate_incidents(sites_df, buildings_df, assets_df, people_df, contractors_df, site_contractors_df, seed=47):
    """Generate incidents for all sites over the full date range."""
    rng = np.random.default_rng(seed)
    template_data = load_narrative_templates()
    incidents = []
    incident_id = 1

    # Pre-index lookups
    people_by_site = people_df.groupby('site_id')['person_id'].apply(list).to_dict()
    buildings_by_site = buildings_df.groupby('site_id', group_keys=False).apply(lambda x: x[['building_id', 'building_name']].to_dict('records'), include_groups=False).to_dict()
    assets_by_site = assets_df.groupby('site_id')['asset_id'].apply(list).to_dict()

    # Build site-contractor lookup
    sc_by_site = site_contractors_df.groupby('site_id')['contractor_id'].apply(list).to_dict()
    contractor_names = contractors_df.set_index('contractor_id')['company_name'].to_dict()

    total_sites = len(sites_df)
    for idx, (_, site) in enumerate(sites_df.iterrows()):
        if idx % 500 == 0:
            print(f"  Processing site {idx}/{total_sites}...")

        site_id = site['site_id']
        site_people = people_by_site.get(site_id, [])
        site_buildings = buildings_by_site.get(site_id, [])
        site_assets = assets_by_site.get(site_id, [])
        site_contractor_ids = sc_by_site.get(site_id, [])

        if not site_people:
            continue

        for year in YEARS:
            if year == 2025:
                num_incidents = rng.integers(INCIDENTS_PER_SCHOOL_PER_YEAR_RANGE[0] // 2,
                                             INCIDENTS_PER_SCHOOL_PER_YEAR_RANGE[1] // 2 + 1)
            else:
                num_incidents = rng.integers(*INCIDENTS_PER_SCHOOL_PER_YEAR_RANGE)

            for _ in range(num_incidents):
                incident_date = generate_incident_date(rng, year)
                reported_date = incident_date + timedelta(hours=int(rng.integers(0, 72)))

                # Decide if linked to building/asset/contractor
                building_id = None
                building_name = None
                asset_id = None
                contractor_id = None
                involves_contractor = False

                # 50% linked to a building
                if site_buildings and rng.random() < 0.5:
                    bldg = site_buildings[int(rng.integers(0, len(site_buildings)))]
                    building_id = bldg['building_id']
                    building_name = bldg['building_name']

                # 20% linked to an asset
                if site_assets and rng.random() < 0.2:
                    asset_id = int(rng.choice(site_assets))

                # 25% involve a contractor
                if site_contractor_ids and rng.random() < 0.25:
                    contractor_id = int(rng.choice(site_contractor_ids))
                    involves_contractor = True

                contractor_name = contractor_names.get(contractor_id, None)

                body_part = rng.choice(BODY_PARTS, p=BODY_PART_WEIGHTS)
                date_str = incident_date.strftime('%d %B %Y')

                # 30% realistic, 70% template
                if rng.random() < 0.3:
                    narrative, n_type, n_severity, n_location, n_activity, n_root_cause = \
                        generate_realistic_narrative(template_data, rng, site, building_name, contractor_name, body_part, date_str)
                    incident_type = n_type or rng.choice(INCIDENT_TYPES, p=INCIDENT_TYPE_WEIGHTS)
                    severity = n_severity or rng.choice(SEVERITY_LEVELS, p=SEVERITY_WEIGHTS)
                    location_type = n_location or rng.choice(LOCATION_TYPES, p=LOCATION_TYPE_WEIGHTS)
                    activity = n_activity or rng.choice(ACTIVITIES, p=ACTIVITY_WEIGHTS)
                    root_cause = n_root_cause or rng.choice(ROOT_CAUSES, p=ROOT_CAUSE_WEIGHTS)
                else:
                    narrative = generate_template_narrative(template_data, rng, body_part)
                    incident_type = rng.choice(INCIDENT_TYPES, p=INCIDENT_TYPE_WEIGHTS)
                    severity = rng.choice(SEVERITY_LEVELS, p=SEVERITY_WEIGHTS)
                    location_type = rng.choice(LOCATION_TYPES, p=LOCATION_TYPE_WEIGHTS)
                    activity = rng.choice(ACTIVITIES, p=ACTIVITY_WEIGHTS)
                    root_cause = rng.choice(ROOT_CAUSES, p=ROOT_CAUSE_WEIGHTS)

                # Days lost based on severity
                if severity == 'MINOR':
                    days_lost = 0
                elif severity == 'MODERATE':
                    days_lost = int(rng.integers(1, 5))
                elif severity == 'SERIOUS_HARM':
                    days_lost = int(rng.integers(5, 30))
                else:
                    days_lost = int(rng.integers(10, 60))

                # Investigation status weighted by age
                days_ago = (datetime(2025, 6, 30) - incident_date).days
                if days_ago > 180:
                    inv_status = rng.choice(INVESTIGATION_STATUSES, p=[0.05, 0.10, 0.85])
                elif days_ago > 30:
                    inv_status = rng.choice(INVESTIGATION_STATUSES, p=[0.15, 0.30, 0.55])
                else:
                    inv_status = rng.choice(INVESTIGATION_STATUSES, p=[0.40, 0.40, 0.20])

                reporter = int(rng.choice(site_people))

                incidents.append({
                    'incident_id': incident_id,
                    'site_id': site_id,
                    'building_id': building_id,
                    'asset_id': asset_id,
                    'contractor_id': contractor_id,
                    'reported_by_person_id': reporter,
                    'incident_date': incident_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'reported_date': reported_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'incident_type': incident_type,
                    'severity': severity,
                    'body_part_affected': body_part if incident_type == 'INJURY' else None,
                    'activity_at_time': activity,
                    'location_type': location_type,
                    'narrative': narrative,
                    'root_cause_category': root_cause,
                    'corrective_action_taken': None,  # Some left blank intentionally
                    'investigation_status': inv_status,
                    'days_lost': days_lost,
                    'involves_contractor': involves_contractor,
                })
                incident_id += 1

    return pd.DataFrame(incidents)


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Loading source data...")
    sites = pd.read_csv(os.path.join(OUTPUT_DIR, 'site.csv'))
    buildings = pd.read_csv(os.path.join(OUTPUT_DIR, 'building.csv'))
    assets = pd.read_csv(os.path.join(OUTPUT_DIR, 'asset.csv'))
    people = pd.read_csv(os.path.join(OUTPUT_DIR, 'person.csv'))
    contractors = pd.read_csv(os.path.join(OUTPUT_DIR, 'contractor.csv'))
    site_contractors = pd.read_csv(os.path.join(OUTPUT_DIR, 'site_contractor.csv'))

    print("Generating incidents...")
    incidents = generate_incidents(sites, buildings, assets, people, contractors, site_contractors)
    incidents.to_csv(os.path.join(OUTPUT_DIR, 'incident.csv'), index=False)
    print(f"Generated {len(incidents)} incidents")
