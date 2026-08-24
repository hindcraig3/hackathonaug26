"""Load generated CSV data into Snowflake using PUT + COPY INTO via internal stage."""
import os
from snowflake.connector import connect

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')

# Table load order (respects FK dependencies)
LOAD_ORDER = [
    ('site.csv', 'SITE'),
    ('building.csv', 'BUILDING'),
    ('asset.csv', 'ASSET'),
    ('person.csv', 'PERSON'),
    ('contractor.csv', 'CONTRACTOR'),
    ('site_contractor.csv', 'SITE_CONTRACTOR'),
    ('hazard.csv', 'HAZARD'),
    ('incident.csv', 'INCIDENT'),
    ('risk_assessment.csv', 'RISK_ASSESSMENT'),
    ('inspection.csv', 'INSPECTION'),
    ('action_item.csv', 'ACTION_ITEM'),
]

DATABASE = 'HS_WORKSHOP'
SCHEMA = 'RAW'
STAGE = 'DATAFILES'


def get_connection():
    """Create Snowflake connection using default connection config."""
    return connect(
        connection_name='default',
        database=DATABASE,
        schema=SCHEMA,
    )


def load_all(data_dict=None):
    """Load all CSV files to Snowflake via PUT to stage then COPY INTO.

    Args:
        data_dict: Ignored (kept for API compatibility). Loading always reads from CSV files.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"USE DATABASE {DATABASE}")
        cursor.execute(f"USE SCHEMA {SCHEMA}")

        for csv_file, table_name in LOAD_ORDER:
            csv_path = os.path.join(OUTPUT_DIR, csv_file)
            if not os.path.exists(csv_path):
                print(f"  SKIP - {csv_file} not found")
                continue

            print(f"  Loading {table_name}...")

            # Truncate table before loading
            cursor.execute(f"TRUNCATE TABLE IF EXISTS {table_name}")

            # PUT file to internal stage (subfolder per table)
            put_sql = f"PUT 'file://{csv_path}' @{STAGE}/{table_name}/ AUTO_COMPRESS=TRUE OVERWRITE=TRUE"
            cursor.execute(put_sql)
            put_result = cursor.fetchone()
            print(f"    PUT: {put_result[0]} -> {put_result[6]}")

            # COPY INTO table from stage
            copy_sql = f"""
                COPY INTO {table_name}
                FROM @{STAGE}/{table_name}/
                FILE_FORMAT = CSV_FORMAT
                MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
                ON_ERROR = 'CONTINUE'
            """
            cursor.execute(copy_sql)
            copy_result = cursor.fetchone()
            rows_loaded = copy_result[3] if copy_result else 0
            errors = copy_result[5] if copy_result else 0
            print(f"    COPY: {rows_loaded} rows loaded, {errors} errors")

        print("\nAll tables loaded successfully!")

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    load_all()
