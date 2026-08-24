# Setup & Data Generation Guide

## Prerequisites

- Python 3.9+
- `pandas` and `numpy` packages
- `snowflake-connector-python` (for loading to Snowflake)

Install dependencies:

```bash
pip install pandas numpy snowflake-connector-python
```

## Step 1: Generate CSV Data

From the project root:

```bash
cd generators
python run_generators.py
```

This runs all generators in dependency order and writes CSV files to the `output/` directory. Expect it to take 3-5 minutes for the full dataset (~2,565 schools).

Output files created:

| File | Approx Rows | Description |
|------|-------------|-------------|
| `site.csv` | 2,565 | NZ schools from the directory |
| `building.csv` | ~15,000 | 5-12 buildings per school |
| `asset.csv` | ~38,000 | Equipment, infrastructure, vehicles |
| `person.csv` | ~9,000 | Synthetic H&S staff (3-4 per school) |
| `contractor.csv` | 150 | Synthetic service companies |
| `site_contractor.csv` | ~10,000 | Contractor-to-school assignments |
| `incident.csv` | ~100,000 | Workplace incidents (5 years) |
| `risk_assessment.csv` | ~28,000 | Scheduled assessments (2/year) |
| `inspection.csv` | ~16,000 | Ad-hoc site inspections |
| `hazard.csv` | ~50,000 | Hazard register entries |
| `action_item.csv` | ~80,000 | Corrective actions |

## Step 2: Create Snowflake Tables

Run the DDL script against your Snowflake account. This creates the `HS_WORKSHOP` database, `RAW` schema, and all 11 tables:

```sql
-- In Snowflake (Snowsight, SnowSQL, or via connector)
-- Execute the contents of: ddl/create_tables.sql
```

Or via SnowSQL:

```bash
snowsql -f ddl/create_tables.sql
```

## Step 3: Load Data to Snowflake

After generating CSVs and creating tables:

```bash
cd generators
python run_generators.py --load
```

This uses `snowflake-connector-python` with `write_pandas` to load each table. It truncates tables before loading so it is safe to re-run.

The loader uses the default Snowflake connection from your `~/.snowflake/connections.toml`. Ensure you have a connection configured with appropriate permissions to create databases and write data.

## Snowflake Connection

The loader expects a default connection in `~/.snowflake/connections.toml`:

```toml
[default]
account = "your-account"
user = "your-user"
authenticator = "externalbrowser"  # or password, keypair, etc.
warehouse = "your-warehouse"
```

## Data Model Overview

```
SITE (school)
 ├── BUILDING (classrooms, gyms, halls)
 ├── ASSET (equipment, playground, vehicles)
 ├── PERSON (principal, site manager, H&S rep, caretaker)
 ├── SITE_CONTRACTOR → CONTRACTOR (service companies)
 ├── INCIDENT (injuries, near-misses, property damage)
 ├── RISK_ASSESSMENT (scheduled, 2/year)
 ├── INSPECTION (ad-hoc, post-incident, contractor audits)
 ├── HAZARD (identified risks — linked to building, asset, or environment)
 └── ACTION_ITEM (corrective actions from assessments/inspections)
```

Key relationships:
- Hazards can be linked to a building, an asset, or neither (physical environment like trees, waterways, roads)
- Incidents can involve a contractor or not (e.g. a teacher slipping on stairs)
- Action items trace back to either a risk assessment or an inspection
- Contractors are rated A-D on safety performance

## Regenerating Data

All generators use fixed random seeds for reproducibility. To generate different data, change the `seed` parameter in each generator's function call within `run_generators.py`.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'config'`** — Make sure you run from the `generators/` directory
- **Snowflake connection errors** — Check your `~/.snowflake/connections.toml` is configured
- **Memory issues** — The incident generator processes all schools sequentially; if memory is tight, reduce `INCIDENTS_PER_SCHOOL_PER_YEAR_RANGE` in `config.py`
