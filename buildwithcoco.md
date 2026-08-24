# Build with CoCo: Leadership needs proactive insights into Health and Safety


## What is needed from you

The organisation has a responsibility to manage health and safety across more than 2000 schools in New Zealand. They have identified two major areas where they need better insights into Health and Safety.  The data and insights team (thats you) have been tasked with rapidly developing a MVP solution that will address 1, or both key themes. The leadership team assumed it would take months but the Chief Data Officer said you could build a MVP in a day. 

Today you need to:


👩‍💻 **Design and Build a prototype solution to provide the LT with better insights**

🧑‍🏫 **Provide a 5-7 minute showcase of your solution**


## How can this be done in a day?

You will leverage ❄️ **Snowflake** ❄️ and ❄️**Snowflake CoCo**❄️ to rapidly design and build your solution.  You get to choose what you want to build. 

- Want to build an Interactive Streamlit application to all the LT to slice and dice the data? Go for it.
- Want to train machine leaning model to create a risk score for each site? Sounds cool. CoCo loves ML
- Need to ingest or generate some new data to make your demo pop? CoCo can help here to.
- Want to allow the leadership team to ask Natural language questions via a chat interface? CoCo builds agents. 
- Want to build a beautiful HTML presentation that could be used at the next board meeting to present key Health and safety KPI's and metrics? Yup...CoCo
- Need to document your solution and the architecture? CoCo also does the boring stuff.

## Where do we start?

Heres a high level workflow you might want to follow :

1. Ask CoCo to help understand what kind of insights might be useful to meet the business needs? or explore why the business really needs to have better insights? 💡**HINT:** this may be useful for to help frame up your demonstration
2. Use CoCo to help you design some more detailed requirements? 
3. Ask CoCo to take your more detailed requirements and design a solution 💡**HINT:** Use **Plan** mode in CoCo
4. Once you have refined your Plan get CoCo to built it. 
5. Test it. Use CoCo to fix bugs, make refinements, add new features. 
6. Use CoCo to help create a presentation if you want one for your demo. 💡**HINT:** CoCO is not bad at creating HTML presentations. 

---

### Theme 1: Incident Insights

**Business Context:** "Our organisation records workplace incidents across multiple sites and regions, but we lack the ability to quickly understand what's happening, where, and why. Leadership wants to move from reactive reporting to proactive insight."

**Business Needs:**

1. **Trend & Pattern Analysis** — Identify emerging patterns in incident frequency, severity, and type across time, location, team, and activity. Detect when a site or region is trending upward in near-misses before a serious harm event occurs.

2. **Incident Classification & Summarisation** — Incident narratives are free-text and inconsistently categorised by reporters. Automatically classify incidents by type, body part affected, root cause category, and generate concise summaries for leadership reporting.

3. **Self-Service Questioning** — Enable non-technical managers and regional leaders to ask natural-language questions about incident data (e.g., "How many serious harm incidents occurred in the Wellington region this quarter?" or "What are the top 3 incident types for contractor staff?") and receive trustworthy answers.

**Example questions teams should enable:**
- What are the incident trends by month, region, and severity over the past 12 months?
- Which sites have a disproportionate share of serious harm vs. near-miss incidents?
- Are there seasonal or day-of-week patterns in certain incident types?
- What are the most common root causes extracted from incident narratives?
- Summarise all incidents at Site X in the last 90 days.

---

### Theme 2: Hazard Management

**Business Context:** "We have obligations as a PCBU under the Health and Safety at Work Act to manage workplace risks. We conduct risk assessments, site inspections, and track hazards — but it's hard to see the full picture across hundreds of sites, dozens of contractors, and thousands of open action items."

**Business Needs:**

1. **Site Risk Visibility** — Provide a composite view of each site's risk posture based on inspection results, open hazards, incident history, and time-since-last-assessment. Enable prioritisation of inspection resources toward highest-risk sites.

2. **Action Item Accountability** — Surface overdue corrective actions from risk assessments and inspections. Show who owns them, how long they've been overdue, and enable escalation visibility.

3. **Hazard Extraction from Field Notes** — Inspectors write unstructured field notes during site visits. Automatically extract mentioned hazards, affected equipment/areas, and suggested controls from those notes to enrich the hazard register.

4. **Contractor Safety Performance** — Consolidate each contractor's safety record across all sites — incidents attributed to them, inspection non-compliances, expired certifications — into a single performance view to inform procurement decisions.

5. **Self-Service Questioning** — Enable managers to ask natural-language questions about hazard and risk data (e.g., "Which sites have overdue high-risk actions?" or "What is Contractor X's safety record this year?").

**Example questions teams should enable:**
- Which 10 sites have the highest composite risk score right now?
- How many high/critical actions are overdue by more than 30 days, and who owns them?
- Which contractors have the worst safety performance relative to hours worked?
- What hazards were identified in the last round of inspections at Region Y?
- When was Site Z last assessed, and what were the findings?

---

## 📗 Build with CoCo Set up

**NOTE: if you are working in a team only 1 person needs to do this**

### 1. Set up Database and tables
1. Download the 2 SQL files and the ZIP file from the [**Assets** ](/assets/) folder
2. Unzip the **data_files.zip** zip file. The unzipped folder will contain the 11 data files you need to upload.
1. Login to Snowflake and select **Projects** then **Workspaces** from the left hand menu. 
1. Click the **+ Add New** button and select **Upload Files**.
1. Select the **2 SQL files**. Once uploaded they should appear in your workspaces file list
1. Open **01_create_tables.sql**
1. In the worksheet click the down arrow next to the blue **Run** button and select **Run All**.  This will run all the statements in the script which will set up you database, schema and tables.  Once completed you need to upload the data files

### 2. Upload data files
1. In the left hand menu select **Ingestion** then **Add Data**
1. Click the **Load files to stage** button
1. Click the browse button, then locate the data files you unzipped early. Select all the data files and click **upload**
1. Then set the database, schema and stage for the destination:\
**DATABASE:** HS_Workshop\
**SCHEMA:** RAW\
S**TAGE:** DATAFILES
1. Leave the "path" field as is, then click the **UPLOAD** button
1. An Upload progress indicator will appear in the bottom right hand corner of the page. 
1. Once complete you will get the follow confirmation: **11 files successfully uploaded to DATAFILES**

### 3. Load data into tables
1. Login to Snowflake and select **Projects** then **Workspaces** from the left hand menu.  
1. Open the **02_dataload.sql** file 
1. In the worksheet click the down arrow next to the blue **Run** button and select **Run All**.  This will run all the statements in the script which will load the data from the files you just uploaded.
1. Once complete the results should show 11 tables and the row count of each table. 

### ✅ You are now good to begin your build
---