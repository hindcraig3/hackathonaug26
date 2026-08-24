"""Generate BUILDING table - assign buildings to each school based on size."""
import pandas as pd
import numpy as np
import os
from config import (
    BUILDING_CONFIG, BUILDING_TYPES, BUILDING_NAMES, CONDITION_RATINGS, CONDITION_WEIGHTS
)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')


def get_school_size(total_roll: int) -> str:
    if total_roll >= BUILDING_CONFIG['large']['roll_threshold']:
        return 'large'
    elif total_roll >= BUILDING_CONFIG['medium']['roll_threshold']:
        return 'medium'
    return 'small'


def generate_buildings(sites_df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """Generate buildings for each school site."""
    rng = np.random.default_rng(seed)
    buildings = []
    building_id = 1

    for _, site in sites_df.iterrows():
        size = get_school_size(site['total_roll'])
        config = BUILDING_CONFIG[size]
        num_buildings = rng.integers(config['min'], config['max'] + 1)

        # Every school gets at least: CLASSROOM, ADMIN, TOILET_BLOCK
        required = ['CLASSROOM', 'ADMIN', 'TOILET_BLOCK']
        available_types = [t for t in BUILDING_TYPES if t not in required]
        extra_count = max(0, num_buildings - len(required))
        extra_types = rng.choice(available_types, size=min(extra_count, len(available_types)), replace=False).tolist()

        # Large schools get multiple classrooms
        building_types_for_site = required + extra_types
        if size == 'large':
            building_types_for_site += ['CLASSROOM'] * rng.integers(2, 4)
        elif size == 'medium':
            building_types_for_site += ['CLASSROOM'] * rng.integers(1, 3)

        for btype in building_types_for_site[:num_buildings]:
            names = BUILDING_NAMES.get(btype, [btype.replace('_', ' ').title()])
            name = rng.choice(names)
            year_built = rng.integers(1950, 2023)
            floor_area = rng.integers(50, 800) if btype != 'STORAGE' else rng.integers(20, 100)
            num_floors = 1 if btype in ('STORAGE', 'TOILET_BLOCK', 'SPORTS_PAVILION') else rng.integers(1, 3)
            condition = rng.choice(CONDITION_RATINGS, p=CONDITION_WEIGHTS)

            buildings.append({
                'building_id': building_id,
                'site_id': site['site_id'],
                'building_name': name,
                'building_type': btype,
                'year_built': int(year_built),
                'floor_area_sqm': int(floor_area),
                'num_floors': int(num_floors),
                'condition_rating': condition,
                'last_assessed_date': pd.Timestamp('2020-01-01') + pd.Timedelta(days=int(rng.integers(0, 1800))),
            })
            building_id += 1

    return pd.DataFrame(buildings)


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sites = pd.read_csv(os.path.join(OUTPUT_DIR, 'site.csv'))
    buildings = generate_buildings(sites)
    buildings.to_csv(os.path.join(OUTPUT_DIR, 'building.csv'), index=False)
    print(f"Generated {len(buildings)} buildings across {len(sites)} sites")
