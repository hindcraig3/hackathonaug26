"""Generate SITE table from school_directory.csv."""
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')


def generate_sites() -> pd.DataFrame:
    """Load school directory and transform to SITE table format."""
    csv_path = os.path.join(DATA_DIR, 'school_directory.csv')
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    # Filter to open schools only
    df = df[df['Status'] == 'Open'].copy()

    sites = pd.DataFrame({
        'site_id': df['School Number'].astype(int),
        'site_name': df['School Name'],
        'street_address': df['Street'],
        'suburb': df['Suburb'],
        'town_city': df['Town / City'],
        'postal_code': df['Postal Code'].astype(str),
        'latitude': df['Latitude'],
        'longitude': df['Longitude'],
        'location': df.apply(
            lambda r: f"POINT({r['Longitude']} {r['Latitude']})"
            if pd.notna(r['Longitude']) and pd.notna(r['Latitude'])
            else None, axis=1
        ),
        'region': df['Regional Council'],
        'territorial_authority': df['Territorial Authority'],
        'education_region': df['Education Region'],
        'urban_rural': df['Urban/Rural'],
        'school_type': df['School Type'],
        'school_definition': df['Definition'],
        'authority': df['Authority'],
        'total_roll': pd.to_numeric(df['Total School Roll'], errors='coerce').fillna(0).astype(int),
        'equity_index': pd.to_numeric(df['Equity Index (EQI)'], errors='coerce').fillna(0).astype(int),
        'status': 'Open',
    })

    return sites.reset_index(drop=True)


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sites = generate_sites()
    sites.to_csv(os.path.join(OUTPUT_DIR, 'site.csv'), index=False)
    print(f"Generated {len(sites)} sites")
