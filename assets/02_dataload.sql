-- =============================================================================
-- Data Load Script - Load CSVs from @DATAFILES stage into tables
-- =============================================================================
-- Prerequisites:
--   1. Run ddl/create_tables.sql to create database, schema, stage, and tables
--   2. Upload CSV files to the DATAFILES stage using PUT or the Snowsight UI
--      e.g. PUT 'file:///path/to/output/site.csv' @DATAFILES/SITE/ OVERWRITE=TRUE;
-- =============================================================================

USE DATABASE HS_WORKSHOP;
USE SCHEMA RAW;

-- -----------------------------------------------------------------------------
-- Load tables in FK dependency order
-- -----------------------------------------------------------------------------

COPY INTO SITE (site_id, site_name, street_address, suburb, town_city, postal_code,
    latitude, longitude, location, region, territorial_authority, education_region,
    urban_rural, school_type, school_definition, authority, total_roll, equity_index, status)
FROM @DATAFILES/site.csv
FILE_FORMAT = CSV_FORMAT
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

COPY INTO BUILDING (building_id, site_id, building_name, building_type, year_built,
    floor_area_sqm, num_floors, condition_rating, last_assessed_date)
FROM @DATAFILES/building.csv
FILE_FORMAT = CSV_FORMAT
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

COPY INTO ASSET (asset_id, site_id, building_id, asset_name, asset_type,
    install_date, last_service_date, condition_rating, is_active)
FROM @DATAFILES/asset.csv
FILE_FORMAT = CSV_FORMAT
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

COPY INTO PERSON (person_id, site_id, first_name, last_name, role,
    email, phone, start_date, is_active)
FROM @DATAFILES/person.csv
FILE_FORMAT = CSV_FORMAT
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

COPY INTO CONTRACTOR (contractor_id, company_name, service_type, region,
    certification_expiry, is_active, safety_rating)
FROM @DATAFILES/contractor.csv
FILE_FORMAT = CSV_FORMAT
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

COPY INTO SITE_CONTRACTOR (site_contractor_id, site_id, contractor_id,
    contract_start_date, contract_end_date, is_active)
FROM @DATAFILES/site_contractor.csv
FILE_FORMAT = CSV_FORMAT
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

COPY INTO HAZARD (hazard_id, site_id, building_id, asset_id, hazard_type,
    hazard_category, description, location_description, risk_level, status,
    identified_date, identified_by_assessment_id, identified_by_inspection_id,
    control_measures)
FROM @DATAFILES/hazard.csv
FILE_FORMAT = CSV_FORMAT
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

COPY INTO INCIDENT (incident_id, site_id, building_id, asset_id, contractor_id,
    reported_by_person_id, incident_date, reported_date, incident_type, severity,
    body_part_affected, activity_at_time, location_type, narrative,
    root_cause_category, corrective_action_taken, investigation_status,
    days_lost, involves_contractor)
FROM @DATAFILES/incident.csv
FILE_FORMAT = CSV_FORMAT
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

COPY INTO RISK_ASSESSMENT (assessment_id, site_id, conducted_by_person_id,
    assessment_date, assessment_period, overall_risk_score, findings_summary,
    num_hazards_identified, num_actions_created, status)
FROM @DATAFILES/risk_assessment.csv
FILE_FORMAT = CSV_FORMAT
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

COPY INTO INSPECTION (inspection_id, site_id, conducted_by_person_id, contractor_id,
    inspection_date, inspection_type, field_notes, compliance_rating,
    num_hazards_identified, num_actions_created, status)
FROM @DATAFILES/inspection.csv
FILE_FORMAT = CSV_FORMAT
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

COPY INTO ACTION_ITEM (action_id, site_id, hazard_id, assessment_id, inspection_id,
    assigned_to_person_id, action_description, priority, due_date, completed_date,
    status, created_date, notes)
FROM @DATAFILES/action_item.csv
FILE_FORMAT = CSV_FORMAT
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

-- -----------------------------------------------------------------------------
-- Verification: Row counts for all tables
-- -----------------------------------------------------------------------------

SELECT 'SITE' AS table_name, COUNT(*) AS row_count FROM SITE
UNION ALL
SELECT 'BUILDING', COUNT(*) FROM BUILDING
UNION ALL
SELECT 'ASSET', COUNT(*) FROM ASSET
UNION ALL
SELECT 'PERSON', COUNT(*) FROM PERSON
UNION ALL
SELECT 'CONTRACTOR', COUNT(*) FROM CONTRACTOR
UNION ALL
SELECT 'SITE_CONTRACTOR', COUNT(*) FROM SITE_CONTRACTOR
UNION ALL
SELECT 'HAZARD', COUNT(*) FROM HAZARD
UNION ALL
SELECT 'INCIDENT', COUNT(*) FROM INCIDENT
UNION ALL
SELECT 'RISK_ASSESSMENT', COUNT(*) FROM RISK_ASSESSMENT
UNION ALL
SELECT 'INSPECTION', COUNT(*) FROM INSPECTION
UNION ALL
SELECT 'ACTION_ITEM', COUNT(*) FROM ACTION_ITEM
ORDER BY table_name;
