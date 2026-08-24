-- =============================================================================
-- H&S Workshop Data Model - NZ Schools
-- =============================================================================

CREATE DATABASE IF NOT EXISTS HS_WORKSHOP;
USE DATABASE HS_WORKSHOP;

CREATE SCHEMA IF NOT EXISTS RAW;
USE SCHEMA RAW;

-- -----------------------------------------------------------------------------
-- File Format and Internal Stage for data loading
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FILE FORMAT CSV_FORMAT
    TYPE = 'CSV'
    PARSE_HEADER = TRUE
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('', 'NULL');
    COMMENT = 'Standard CSV format for loading generated workshop data';

CREATE OR REPLACE STAGE DATAFILES
    FILE_FORMAT = CSV_FORMAT
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'Internal stage for loading generated CSV data files';

-- -----------------------------------------------------------------------------
-- 1. SITE - sourced from school_directory.csv
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE SITE (
    site_id             INT             NOT NULL PRIMARY KEY COMMENT 'Unique school identifier from the NZ Ministry of Education school number',
    site_name           VARCHAR(200)    NOT NULL COMMENT 'Official name of the school',
    street_address      VARCHAR(300)    COMMENT 'Physical street address of the school',
    suburb              VARCHAR(100)    COMMENT 'Suburb where the school is located',
    town_city           VARCHAR(100)    COMMENT 'Town or city where the school is located',
    postal_code         VARCHAR(10)     COMMENT 'NZ postal code for the school address',
    latitude            FLOAT           COMMENT 'Geographic latitude coordinate (WGS84)',
    longitude           FLOAT           COMMENT 'Geographic longitude coordinate (WGS84)',
    location            GEOGRAPHY       COMMENT 'Point geometry for geospatial queries, constructed from latitude and longitude (WKT format)',
    region              VARCHAR(100)    COMMENT 'NZ Regional Council area (e.g. Auckland Region, Canterbury Region)',
    territorial_authority VARCHAR(100)  COMMENT 'Local territorial authority (district or city council)',
    education_region    VARCHAR(100)    COMMENT 'Ministry of Education administrative region',
    urban_rural         VARCHAR(50)     COMMENT 'Urban/rural classification (e.g. Main urban area, Rural settlement)',
    school_type         VARCHAR(100)    COMMENT 'Type of school (e.g. Primary, Secondary, Composite, Intermediate)',
    school_definition   VARCHAR(200)    COMMENT 'Detailed definition of the school type and year levels',
    authority           VARCHAR(50)     COMMENT 'Governing authority (State, State-Integrated, Private)',
    total_roll          INT             COMMENT 'Total number of enrolled students',
    equity_index        INT             COMMENT 'Equity Index (EQI) score indicating socioeconomic context (lower = more disadvantaged)',
    status              VARCHAR(20)     DEFAULT 'Open' COMMENT 'Operational status of the school (Open or Closed)'
)
COMMENT = 'NZ Schools acting as managed sites for H&S purposes. Sourced from the Ministry of Education school directory.';

-- -----------------------------------------------------------------------------
-- 2. BUILDING
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE BUILDING (
    building_id         INT             NOT NULL PRIMARY KEY COMMENT 'Unique identifier for the building',
    site_id             INT             NOT NULL COMMENT 'FK to SITE - the school this building belongs to',
    building_name       VARCHAR(100)    NOT NULL COMMENT 'Descriptive name of the building (e.g. Block A, Main Gymnasium)',
    building_type       VARCHAR(50)     NOT NULL COMMENT 'Category of building: CLASSROOM, GYM, LIBRARY, ADMIN, HALL, WORKSHOP, STORAGE, TOILET_BLOCK, SPORTS_PAVILION',
    year_built          INT             COMMENT 'Year the building was originally constructed',
    floor_area_sqm      INT             COMMENT 'Total floor area of the building in square metres',
    num_floors          INT             DEFAULT 1 COMMENT 'Number of storeys in the building',
    condition_rating    VARCHAR(20)     COMMENT 'Current assessed condition: GOOD, FAIR, POOR, or CRITICAL',
    last_assessed_date  DATE            COMMENT 'Date the building condition was last formally assessed',
    CONSTRAINT fk_building_site FOREIGN KEY (site_id) REFERENCES SITE(site_id)
)
COMMENT = 'Physical buildings within each school site';

-- -----------------------------------------------------------------------------
-- 3. ASSET
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE ASSET (
    asset_id            INT             NOT NULL PRIMARY KEY COMMENT 'Unique identifier for the asset',
    site_id             INT             NOT NULL COMMENT 'FK to SITE - the school this asset belongs to',
    building_id         INT             COMMENT 'FK to BUILDING - NULL if this is an outdoor or grounds-level asset',
    asset_name          VARCHAR(200)    NOT NULL COMMENT 'Descriptive name of the asset (e.g. Ride-on Mower #2, Junior Playground)',
    asset_type          VARCHAR(50)     NOT NULL COMMENT 'Category: HVAC, ELECTRICAL, PLAYGROUND, VEHICLE, GROUNDS_EQUIPMENT, MACHINERY, CAR_PARK, BUS_STOP, SPORTS_EQUIPMENT, FENCING, ROOFING',
    install_date        DATE            COMMENT 'Date the asset was installed or first put into service',
    last_service_date   DATE            COMMENT 'Date of the most recent maintenance or servicing',
    condition_rating    VARCHAR(20)     COMMENT 'Current assessed condition: GOOD, FAIR, POOR, or CRITICAL',
    is_active           BOOLEAN         DEFAULT TRUE COMMENT 'Whether the asset is currently in active use (FALSE if decommissioned)',
    CONSTRAINT fk_asset_site FOREIGN KEY (site_id) REFERENCES SITE(site_id),
    CONSTRAINT fk_asset_building FOREIGN KEY (building_id) REFERENCES BUILDING(building_id)
)
COMMENT = 'Physical assets at each school - equipment, infrastructure, vehicles, and grounds features';

-- -----------------------------------------------------------------------------
-- 4. PERSON - synthetic owners/assignees
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE PERSON (
    person_id           INT             NOT NULL PRIMARY KEY COMMENT 'Unique identifier for the person',
    site_id             INT             NOT NULL COMMENT 'FK to SITE - the school where this person is primarily based',
    first_name          VARCHAR(50)     NOT NULL COMMENT 'First name of the person (synthetic)',
    last_name           VARCHAR(50)     NOT NULL COMMENT 'Last name of the person (synthetic)',
    role                VARCHAR(50)     NOT NULL COMMENT 'H&S role at the school: PRINCIPAL, SITE_MANAGER, HS_REP, or CARETAKER',
    email               VARCHAR(200)    COMMENT 'Work email address (synthetic)',
    phone               VARCHAR(20)     COMMENT 'Contact phone number (synthetic)',
    start_date          DATE            COMMENT 'Date the person started in this role at the school',
    is_active           BOOLEAN         DEFAULT TRUE COMMENT 'Whether the person is currently active in this role',
    CONSTRAINT fk_person_site FOREIGN KEY (site_id) REFERENCES SITE(site_id)
)
COMMENT = 'Synthetic staff responsible for H&S duties at each school - owners and assignees of actions and assessments';

-- -----------------------------------------------------------------------------
-- 5. CONTRACTOR
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE CONTRACTOR (
    contractor_id       INT             NOT NULL PRIMARY KEY COMMENT 'Unique identifier for the contractor company',
    company_name        VARCHAR(200)    NOT NULL COMMENT 'Name of the contractor company (synthetic)',
    service_type        VARCHAR(50)     NOT NULL COMMENT 'Primary service category: BUILDING_MAINTENANCE, ELECTRICAL, PLUMBING, CLEANING, GROUNDS, IT_SERVICES, PAINTING, ROOFING, SECURITY, HVAC',
    region              VARCHAR(100)    COMMENT 'Primary NZ region where the contractor operates',
    certification_expiry DATE           COMMENT 'Date when the contractor safety certification expires',
    is_active           BOOLEAN         DEFAULT TRUE COMMENT 'Whether the contractor is currently active and available for work',
    safety_rating       VARCHAR(5)      COMMENT 'Overall safety performance rating: A (best) through D (worst)'
)
COMMENT = 'Synthetic contractor companies providing maintenance, construction, and specialist services to schools';

-- -----------------------------------------------------------------------------
-- 6. SITE_CONTRACTOR (many-to-many junction)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE SITE_CONTRACTOR (
    site_contractor_id  INT             NOT NULL PRIMARY KEY COMMENT 'Unique identifier for this site-contractor relationship',
    site_id             INT             NOT NULL COMMENT 'FK to SITE - the school being serviced',
    contractor_id       INT             NOT NULL COMMENT 'FK to CONTRACTOR - the company providing the service',
    contract_start_date DATE            NOT NULL COMMENT 'Date the contract between the school and contractor commenced',
    contract_end_date   DATE            COMMENT 'Date the contract ended (NULL if still active)',
    is_active           BOOLEAN         DEFAULT TRUE COMMENT 'Whether this contract is currently active',
    CONSTRAINT fk_sc_site FOREIGN KEY (site_id) REFERENCES SITE(site_id),
    CONSTRAINT fk_sc_contractor FOREIGN KEY (contractor_id) REFERENCES CONTRACTOR(contractor_id)
)
COMMENT = 'Junction table linking contractor companies to the school sites they service';

-- -----------------------------------------------------------------------------
-- 7. HAZARD
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE HAZARD (
    hazard_id           INT             NOT NULL PRIMARY KEY COMMENT 'Unique identifier for the hazard',
    site_id             INT             NOT NULL COMMENT 'FK to SITE - the school where this hazard exists',
    building_id         INT             COMMENT 'FK to BUILDING - NULL if hazard relates to the physical environment (trees, waterways, roads)',
    asset_id            INT             COMMENT 'FK to ASSET - NULL if hazard is not related to a specific asset',
    hazard_type         VARCHAR(50)     NOT NULL COMMENT 'Broad hazard classification: PHYSICAL, CHEMICAL, BIOLOGICAL, ERGONOMIC, ENVIRONMENTAL, ELECTRICAL, STRUCTURAL',
    hazard_category     VARCHAR(50)     NOT NULL COMMENT 'Specific hazard category: SLIP_TRIP_FALL, FALLING_OBJECTS, MACHINERY, TRAFFIC, WEATHER, ASBESTOS, WATER, TREES, PLAYGROUND, ELECTRICAL, HEIGHTS',
    description         VARCHAR(2000)   NOT NULL COMMENT 'Detailed free-text description of the hazard and its context',
    location_description VARCHAR(500)   COMMENT 'Specific location of the hazard within the school grounds (e.g. Stairwell Block B, Northern boundary)',
    risk_level          VARCHAR(20)     NOT NULL COMMENT 'Assessed risk level: LOW, MEDIUM, HIGH, or CRITICAL',
    status              VARCHAR(20)     NOT NULL DEFAULT 'OPEN' COMMENT 'Current hazard status: OPEN (uncontrolled), CONTROLLED, ELIMINATED, or MONITORING',
    identified_date     DATE            NOT NULL COMMENT 'Date the hazard was first identified',
    identified_by_assessment_id INT     COMMENT 'FK to RISK_ASSESSMENT - if hazard was found during a scheduled risk assessment',
    identified_by_inspection_id INT     COMMENT 'FK to INSPECTION - if hazard was found during an ad-hoc inspection',
    control_measures    VARCHAR(2000)   COMMENT 'Description of control measures applied to manage the hazard',
    CONSTRAINT fk_hazard_site FOREIGN KEY (site_id) REFERENCES SITE(site_id),
    CONSTRAINT fk_hazard_building FOREIGN KEY (building_id) REFERENCES BUILDING(building_id),
    CONSTRAINT fk_hazard_asset FOREIGN KEY (asset_id) REFERENCES ASSET(asset_id)
)
COMMENT = 'Hazard register - known workplace risks at each school site including building, asset, and environmental hazards';

-- -----------------------------------------------------------------------------
-- 8. INCIDENT
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE INCIDENT (
    incident_id         INT             NOT NULL PRIMARY KEY COMMENT 'Unique identifier for the incident',
    site_id             INT             NOT NULL COMMENT 'FK to SITE - the school where the incident occurred',
    building_id         INT             COMMENT 'FK to BUILDING - NULL if the incident occurred outdoors or in the physical environment',
    asset_id            INT             COMMENT 'FK to ASSET - NULL if no specific asset was involved',
    contractor_id       INT             COMMENT 'FK to CONTRACTOR - NULL if no contractor was involved (e.g. teacher slip on stairs)',
    reported_by_person_id INT           NOT NULL COMMENT 'FK to PERSON - the staff member who reported the incident',
    incident_date       TIMESTAMP_NTZ   NOT NULL COMMENT 'Date and time when the incident actually occurred',
    reported_date       TIMESTAMP_NTZ   NOT NULL COMMENT 'Date and time when the incident was formally reported (may be later than occurrence)',
    incident_type       VARCHAR(30)     NOT NULL COMMENT 'Classification of incident: INJURY, NEAR_MISS, PROPERTY_DAMAGE, ENVIRONMENTAL, or SECURITY',
    severity            VARCHAR(20)     NOT NULL COMMENT 'Severity level: MINOR, MODERATE, SERIOUS_HARM, or NOTIFIABLE (requires WorkSafe notification)',
    body_part_affected  VARCHAR(30)     COMMENT 'Body part injured (for INJURY type): HEAD, BACK, HAND, LEG, FOOT, ARM, SHOULDER, KNEE, MULTIPLE, or NA',
    activity_at_time    VARCHAR(30)     COMMENT 'Activity being performed when incident occurred: TEACHING, MAINTENANCE, SPORT, TRANSIT, CLEANING, CONSTRUCTION, PLAY, ADMIN',
    location_type       VARCHAR(30)     COMMENT 'Type of location where incident occurred: INDOOR, OUTDOOR, CARPARK, PLAYGROUND, SPORTS_FIELD, STAIRWELL, WORKSHOP, KITCHEN',
    narrative           VARCHAR(4000)   NOT NULL COMMENT 'Free-text description of the incident including circumstances, sequence of events, and immediate response',
    root_cause_category VARCHAR(30)     COMMENT 'Identified root cause: HUMAN_ERROR, EQUIPMENT_FAILURE, ENVIRONMENTAL, PROCEDURAL, or TRAINING_GAP',
    corrective_action_taken VARCHAR(2000) COMMENT 'Description of immediate corrective actions taken following the incident',
    investigation_status VARCHAR(20)    NOT NULL DEFAULT 'OPEN' COMMENT 'Current investigation status: OPEN, IN_PROGRESS, or CLOSED',
    days_lost           INT             DEFAULT 0 COMMENT 'Number of work/school days lost as a result of the incident (0 for near-misses)',
    involves_contractor BOOLEAN         DEFAULT FALSE COMMENT 'Whether a contractor was involved in or contributed to the incident',
    CONSTRAINT fk_incident_site FOREIGN KEY (site_id) REFERENCES SITE(site_id),
    CONSTRAINT fk_incident_building FOREIGN KEY (building_id) REFERENCES BUILDING(building_id),
    CONSTRAINT fk_incident_asset FOREIGN KEY (asset_id) REFERENCES ASSET(asset_id),
    CONSTRAINT fk_incident_contractor FOREIGN KEY (contractor_id) REFERENCES CONTRACTOR(contractor_id),
    CONSTRAINT fk_incident_person FOREIGN KEY (reported_by_person_id) REFERENCES PERSON(person_id)
)
COMMENT = 'Workplace incidents across all school sites including injuries, near-misses, property damage, and security events';

-- -----------------------------------------------------------------------------
-- 9. RISK_ASSESSMENT (scheduled, 2 per site per year)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE RISK_ASSESSMENT (
    assessment_id       INT             NOT NULL PRIMARY KEY COMMENT 'Unique identifier for the risk assessment',
    site_id             INT             NOT NULL COMMENT 'FK to SITE - the school being assessed',
    conducted_by_person_id INT          NOT NULL COMMENT 'FK to PERSON - the staff member who conducted the assessment',
    assessment_date     DATE            NOT NULL COMMENT 'Date the risk assessment was carried out on site',
    assessment_period   VARCHAR(10)     NOT NULL COMMENT 'Half-year period identifier (e.g. H1_2021 for Jan-Jun, H2_2021 for Jul-Dec)',
    overall_risk_score  INT             NOT NULL COMMENT 'Composite risk score from 1 (lowest risk) to 100 (highest risk)',
    findings_summary    VARCHAR(4000)   NOT NULL COMMENT 'Free-text summary of key findings, concerns, and recommendations from the assessment',
    num_hazards_identified INT          DEFAULT 0 COMMENT 'Count of new hazards identified during this assessment',
    num_actions_created INT             DEFAULT 0 COMMENT 'Count of corrective action items created as a result of this assessment',
    status              VARCHAR(20)     NOT NULL DEFAULT 'COMPLETED' COMMENT 'Assessment workflow status: DRAFT, COMPLETED, or REVIEWED',
    CONSTRAINT fk_ra_site FOREIGN KEY (site_id) REFERENCES SITE(site_id),
    CONSTRAINT fk_ra_person FOREIGN KEY (conducted_by_person_id) REFERENCES PERSON(person_id)
)
COMMENT = 'Scheduled risk assessments conducted twice per year (H1 and H2) at each school site';

-- -----------------------------------------------------------------------------
-- 10. INSPECTION (ad-hoc)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE INSPECTION (
    inspection_id       INT             NOT NULL PRIMARY KEY COMMENT 'Unique identifier for the inspection',
    site_id             INT             NOT NULL COMMENT 'FK to SITE - the school being inspected',
    conducted_by_person_id INT          NOT NULL COMMENT 'FK to PERSON - the staff member who conducted the inspection',
    contractor_id       INT             COMMENT 'FK to CONTRACTOR - populated when this is a contractor safety audit',
    inspection_date     DATE            NOT NULL COMMENT 'Date the inspection was carried out',
    inspection_type     VARCHAR(30)     NOT NULL COMMENT 'Type of inspection: ROUTINE, POST_INCIDENT, CONTRACTOR_AUDIT, or COMPLAINT_RESPONSE',
    field_notes         VARCHAR(4000)   NOT NULL COMMENT 'Unstructured field notes written by the inspector during the site visit',
    compliance_rating   VARCHAR(30)     NOT NULL COMMENT 'Overall compliance outcome: COMPLIANT, MINOR_NON_COMPLIANCE, MAJOR_NON_COMPLIANCE, or CRITICAL',
    num_hazards_identified INT          DEFAULT 0 COMMENT 'Count of new hazards identified during this inspection',
    num_actions_created INT             DEFAULT 0 COMMENT 'Count of corrective action items created as a result of this inspection',
    status              VARCHAR(20)     NOT NULL DEFAULT 'COMPLETED' COMMENT 'Inspection workflow status: DRAFT, COMPLETED, or REVIEWED',
    CONSTRAINT fk_insp_site FOREIGN KEY (site_id) REFERENCES SITE(site_id),
    CONSTRAINT fk_insp_person FOREIGN KEY (conducted_by_person_id) REFERENCES PERSON(person_id),
    CONSTRAINT fk_insp_contractor FOREIGN KEY (contractor_id) REFERENCES CONTRACTOR(contractor_id)
)
COMMENT = 'Ad-hoc site inspections including routine visits, post-incident reviews, contractor audits, and complaint responses';

-- -----------------------------------------------------------------------------
-- 11. ACTION_ITEM
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE ACTION_ITEM (
    action_id           INT             NOT NULL PRIMARY KEY COMMENT 'Unique identifier for the action item',
    site_id             INT             NOT NULL COMMENT 'FK to SITE - the school where this action applies',
    hazard_id           INT             COMMENT 'FK to HAZARD - the hazard this action addresses (if applicable)',
    assessment_id       INT             COMMENT 'FK to RISK_ASSESSMENT - the assessment that created this action (if applicable)',
    inspection_id       INT             COMMENT 'FK to INSPECTION - the inspection that created this action (if applicable)',
    assigned_to_person_id INT           NOT NULL COMMENT 'FK to PERSON - the staff member responsible for completing this action',
    action_description  VARCHAR(2000)   NOT NULL COMMENT 'Description of the corrective action required',
    priority            VARCHAR(20)     NOT NULL COMMENT 'Priority level determining urgency: LOW, MEDIUM, HIGH, or CRITICAL',
    due_date            DATE            NOT NULL COMMENT 'Target date by which the action must be completed',
    completed_date      DATE            COMMENT 'Actual date the action was completed (NULL if still open)',
    status              VARCHAR(20)     NOT NULL DEFAULT 'OPEN' COMMENT 'Current status: OPEN, IN_PROGRESS, OVERDUE, COMPLETED, or CANCELLED',
    created_date        DATE            NOT NULL COMMENT 'Date the action item was created',
    notes               VARCHAR(2000)   COMMENT 'Additional notes or updates on the action item progress',
    CONSTRAINT fk_action_site FOREIGN KEY (site_id) REFERENCES SITE(site_id),
    CONSTRAINT fk_action_hazard FOREIGN KEY (hazard_id) REFERENCES HAZARD(hazard_id),
    CONSTRAINT fk_action_assessment FOREIGN KEY (assessment_id) REFERENCES RISK_ASSESSMENT(assessment_id),
    CONSTRAINT fk_action_inspection FOREIGN KEY (inspection_id) REFERENCES INSPECTION(inspection_id),
    CONSTRAINT fk_action_person FOREIGN KEY (assigned_to_person_id) REFERENCES PERSON(person_id)
)
COMMENT = 'Corrective actions arising from risk assessments, inspections, and hazards with ownership and due date tracking';
