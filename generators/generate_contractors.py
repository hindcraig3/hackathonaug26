"""Generate CONTRACTOR and SITE_CONTRACTOR tables."""
import pandas as pd
import numpy as np
import os
from config import (
    NUM_CONTRACTORS, CONTRACTOR_SERVICE_TYPES, CONTRACTOR_NAME_PREFIXES,
    CONTRACTOR_NAME_SUFFIXES, NZ_REGIONS, SAFETY_RATINGS, SAFETY_RATING_WEIGHTS, START_DATE
)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')


def generate_contractors(seed: int = 45) -> pd.DataFrame:
    """Generate synthetic contractor companies."""
    rng = np.random.default_rng(seed)
    contractors = []

    used_names = set()
    for i in range(1, NUM_CONTRACTORS + 1):
        # Generate unique company name
        while True:
            prefix = rng.choice(CONTRACTOR_NAME_PREFIXES)
            service = rng.choice(CONTRACTOR_SERVICE_TYPES)
            suffix = rng.choice(CONTRACTOR_NAME_SUFFIXES)
            service_word = service.replace('_', ' ').title().split()[0]
            name = f"{prefix} {service_word} {suffix}"
            if name not in used_names:
                used_names.add(name)
                break

        region = rng.choice(NZ_REGIONS)
        cert_expiry = pd.Timestamp('2024-01-01') + pd.Timedelta(days=int(rng.integers(0, 730)))
        is_active = rng.random() > 0.1  # 90% active
        safety = rng.choice(SAFETY_RATINGS, p=SAFETY_RATING_WEIGHTS)

        contractors.append({
            'contractor_id': i,
            'company_name': name,
            'service_type': service,
            'region': region,
            'certification_expiry': cert_expiry.strftime('%Y-%m-%d'),
            'is_active': is_active,
            'safety_rating': safety,
        })

    return pd.DataFrame(contractors)


def generate_site_contractors(sites_df: pd.DataFrame, contractors_df: pd.DataFrame, seed: int = 46) -> pd.DataFrame:
    """Assign contractors to sites based on region matching."""
    rng = np.random.default_rng(seed)
    assignments = []
    sc_id = 1

    for _, site in sites_df.iterrows():
        # Each school has 3-6 contractors
        num_contractors = rng.integers(3, 7)

        # Prefer same-region contractors (70%) but allow cross-region (30%)
        site_region = site.get('region', '')
        region_contractors = contractors_df[contractors_df['region'] == site_region]
        other_contractors = contractors_df[contractors_df['region'] != site_region]

        selected = []
        for _ in range(num_contractors):
            if len(region_contractors) > 0 and rng.random() < 0.7:
                chosen = region_contractors.sample(1, random_state=int(rng.integers(0, 100000)))
            elif len(other_contractors) > 0:
                chosen = other_contractors.sample(1, random_state=int(rng.integers(0, 100000)))
            else:
                chosen = contractors_df.sample(1, random_state=int(rng.integers(0, 100000)))

            contractor_id = int(chosen.iloc[0]['contractor_id'])
            if contractor_id not in selected:
                selected.append(contractor_id)
                start = pd.Timestamp(START_DATE) + pd.Timedelta(days=int(rng.integers(0, 1200)))
                # Some contracts have ended
                if rng.random() < 0.2:
                    end = start + pd.Timedelta(days=int(rng.integers(365, 1095)))
                    is_active = False
                else:
                    end = None
                    is_active = True

                assignments.append({
                    'site_contractor_id': sc_id,
                    'site_id': site['site_id'],
                    'contractor_id': contractor_id,
                    'contract_start_date': start.strftime('%Y-%m-%d'),
                    'contract_end_date': end.strftime('%Y-%m-%d') if end else None,
                    'is_active': is_active,
                })
                sc_id += 1

    return pd.DataFrame(assignments)


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sites = pd.read_csv(os.path.join(OUTPUT_DIR, 'site.csv'))
    contractors = generate_contractors()
    contractors.to_csv(os.path.join(OUTPUT_DIR, 'contractor.csv'), index=False)
    print(f"Generated {len(contractors)} contractors")

    site_contractors = generate_site_contractors(sites, contractors)
    site_contractors.to_csv(os.path.join(OUTPUT_DIR, 'site_contractor.csv'), index=False)
    print(f"Generated {len(site_contractors)} site-contractor assignments")
