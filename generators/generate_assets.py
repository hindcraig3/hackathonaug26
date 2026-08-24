"""Generate ASSET table - assign assets to buildings and sites."""
import pandas as pd
import numpy as np
import os
from config import (
    BUILDING_CONFIG, ASSET_CONFIG, ASSET_TYPES, ASSET_NAMES,
    CONDITION_RATINGS, CONDITION_WEIGHTS
)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')


def get_school_size(total_roll: int) -> str:
    if total_roll >= BUILDING_CONFIG['large']['roll_threshold']:
        return 'large'
    elif total_roll >= BUILDING_CONFIG['medium']['roll_threshold']:
        return 'medium'
    return 'small'


# Assets that go inside buildings
INDOOR_ASSET_TYPES = ['HVAC', 'ELECTRICAL', 'MACHINERY']
# Assets that are outdoor / site-level
OUTDOOR_ASSET_TYPES = ['PLAYGROUND', 'VEHICLE', 'GROUNDS_EQUIPMENT', 'CAR_PARK', 'BUS_STOP', 'SPORTS_EQUIPMENT', 'FENCING', 'ROOFING']


def generate_assets(sites_df: pd.DataFrame, buildings_df: pd.DataFrame, seed: int = 43) -> pd.DataFrame:
    """Generate assets for each school site."""
    rng = np.random.default_rng(seed)
    assets = []
    asset_id = 1

    for _, site in sites_df.iterrows():
        size = get_school_size(site['total_roll'])
        config = ASSET_CONFIG[size]
        num_assets = rng.integers(config['min'], config['max'] + 1)

        site_buildings = buildings_df[buildings_df['site_id'] == site['site_id']]
        building_ids = site_buildings['building_id'].tolist() if len(site_buildings) > 0 else []

        for _ in range(num_assets):
            # 40% indoor (linked to building), 60% outdoor (site-level)
            is_indoor = rng.random() < 0.4 and len(building_ids) > 0

            if is_indoor:
                asset_type = rng.choice(INDOOR_ASSET_TYPES)
                building_id = int(rng.choice(building_ids))
            else:
                asset_type = rng.choice(OUTDOOR_ASSET_TYPES)
                building_id = None

            names = ASSET_NAMES.get(asset_type, [asset_type.replace('_', ' ').title()])
            name = rng.choice(names)
            # Add a number to differentiate
            suffix = f" #{rng.integers(1, 5)}" if rng.random() > 0.5 else ""

            install_date = pd.Timestamp('2005-01-01') + pd.Timedelta(days=int(rng.integers(0, 6500)))
            last_service = install_date + pd.Timedelta(days=int(rng.integers(90, 1800)))
            if last_service > pd.Timestamp('2025-06-30'):
                last_service = pd.Timestamp('2025-06-30') - pd.Timedelta(days=int(rng.integers(30, 365)))

            condition = rng.choice(CONDITION_RATINGS, p=CONDITION_WEIGHTS)
            is_active = condition != 'CRITICAL' or rng.random() > 0.5

            assets.append({
                'asset_id': asset_id,
                'site_id': site['site_id'],
                'building_id': building_id,
                'asset_name': f"{name}{suffix}",
                'asset_type': asset_type,
                'install_date': install_date.strftime('%Y-%m-%d'),
                'last_service_date': last_service.strftime('%Y-%m-%d'),
                'condition_rating': condition,
                'is_active': is_active,
            })
            asset_id += 1

    return pd.DataFrame(assets)


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sites = pd.read_csv(os.path.join(OUTPUT_DIR, 'site.csv'))
    buildings = pd.read_csv(os.path.join(OUTPUT_DIR, 'building.csv'))
    assets = generate_assets(sites, buildings)
    assets.to_csv(os.path.join(OUTPUT_DIR, 'asset.csv'), index=False)
    print(f"Generated {len(assets)} assets across {len(sites)} sites")
