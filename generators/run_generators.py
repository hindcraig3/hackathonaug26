"""
Master data generation and loading script.

Usage:
    python run_generators.py              # Generate CSV files only
    python run_generators.py --load       # Generate and load to Snowflake
"""
import os
import sys
import time

# Add generators dir to path
sys.path.insert(0, os.path.dirname(__file__))

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')


def run_generation():
    """Run all generators in dependency order."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("H&S Workshop Data Generator")
    print("=" * 60)

    # Step 1: Sites
    print("\n[1/6] Generating sites from school directory...")
    start = time.time()
    from generate_sites import generate_sites
    sites = generate_sites()
    sites.to_csv(os.path.join(OUTPUT_DIR, 'site.csv'), index=False)
    print(f"  -> {len(sites)} sites ({time.time()-start:.1f}s)")

    # Step 2: Buildings
    print("\n[2/6] Generating buildings...")
    start = time.time()
    from generate_buildings import generate_buildings
    buildings = generate_buildings(sites)
    buildings.to_csv(os.path.join(OUTPUT_DIR, 'building.csv'), index=False)
    print(f"  -> {len(buildings)} buildings ({time.time()-start:.1f}s)")

    # Step 3: Assets
    print("\n[3/6] Generating assets...")
    start = time.time()
    from generate_assets import generate_assets
    assets = generate_assets(sites, buildings)
    assets.to_csv(os.path.join(OUTPUT_DIR, 'asset.csv'), index=False)
    print(f"  -> {len(assets)} assets ({time.time()-start:.1f}s)")

    # Step 4: People & Contractors
    print("\n[4/6] Generating people and contractors...")
    start = time.time()
    from generate_people import generate_people
    from generate_contractors import generate_contractors, generate_site_contractors
    people = generate_people(sites)
    people.to_csv(os.path.join(OUTPUT_DIR, 'person.csv'), index=False)
    contractors = generate_contractors()
    contractors.to_csv(os.path.join(OUTPUT_DIR, 'contractor.csv'), index=False)
    site_contractors = generate_site_contractors(sites, contractors)
    site_contractors.to_csv(os.path.join(OUTPUT_DIR, 'site_contractor.csv'), index=False)
    print(f"  -> {len(people)} people, {len(contractors)} contractors, {len(site_contractors)} assignments ({time.time()-start:.1f}s)")

    # Step 5: Incidents
    print("\n[5/6] Generating incidents (this may take a few minutes)...")
    start = time.time()
    from generate_incidents import generate_incidents
    incidents = generate_incidents(sites, buildings, assets, people, contractors, site_contractors)
    incidents.to_csv(os.path.join(OUTPUT_DIR, 'incident.csv'), index=False)
    print(f"  -> {len(incidents)} incidents ({time.time()-start:.1f}s)")

    # Step 6: Assessments, Inspections, Hazards, Actions
    print("\n[6/6] Generating assessments, inspections, hazards, actions...")
    start = time.time()
    from generate_assessments import generate_all
    assessments, inspections, hazards, actions = generate_all(
        sites, buildings, assets, people, contractors, site_contractors
    )
    assessments.to_csv(os.path.join(OUTPUT_DIR, 'risk_assessment.csv'), index=False)
    inspections.to_csv(os.path.join(OUTPUT_DIR, 'inspection.csv'), index=False)
    hazards.to_csv(os.path.join(OUTPUT_DIR, 'hazard.csv'), index=False)
    actions.to_csv(os.path.join(OUTPUT_DIR, 'action_item.csv'), index=False)
    print(f"  -> {len(assessments)} assessments, {len(inspections)} inspections, {len(hazards)} hazards, {len(actions)} actions ({time.time()-start:.1f}s)")

    print("\n" + "=" * 60)
    print("Generation complete! CSV files written to: output/")
    print("=" * 60)

    return {
        'sites': sites,
        'buildings': buildings,
        'assets': assets,
        'people': people,
        'contractors': contractors,
        'site_contractors': site_contractors,
        'incidents': incidents,
        'assessments': assessments,
        'inspections': inspections,
        'hazards': hazards,
        'actions': actions,
    }


if __name__ == '__main__':
    data = run_generation()

    if '--load' in sys.argv:
        print("\n\nLoading data to Snowflake...")
        from load_to_snowflake import load_all
        load_all(data)
