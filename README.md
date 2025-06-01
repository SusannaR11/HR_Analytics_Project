HiRe™ – HR Analytics Dashboard 
 
Final Project in Data Engineering 2 @OPA24 (Object Oriented Programming with AI)

Developed as a proof of concept for an interactive HR analytics platform using Streamlit, dbt, DuckDB and Google Gemini.

────────────────────────────
📝 Project Description  
────────────────────────────
HiRe™ is a talent intelligence tool for recruiters, powered by real-time data and AI analysis. It lets you:

- Browse job openings by sector (Data/IT, Social Work, Security)
- Visualize KPIs and trends in job ads
- Analyze job descriptions using LLMs (Gemini) for top hard & soft skills
- Compare role-specific soft skills with field averages using spider charts
- Present insights in HR-report tone, designed for decision-makers

────────────────────────────
🚀 How to Run  
────────────────────────────

Clone the repository:
> git clone https://github.com/StefanLundberg77/hr_analytics_proj.git

Navigate to the project directory:
> cd YOUR-REPO

Create a virtual environment:
> uv venv .venv

Activate it:
- Windows:
  > .venv\Scripts\activate
- macOS/Linux:
  > source .venv/bin/activate

Install dependencies:
- Windows:
  > uv pip install -r requirements.txt
- macOS/Linux:
  > uv pip install -r requirements.mac.txt

Fetch data from the JobAds API, run the script:
 > python load_api.py

Alternatively, open `load_api.py` in your IDE and run it directly.

Run the Streamlit dashboard:

 > streamlit run app.py

────────────────────────────
🔧 Configuration & DuckDB Profile  
────────────────────────────

Set up `profiles.yml` configuration:

project_HiRe: 
  target: dev 
  outputs: 
    dev: 
      type: duckdb
      path: ../ads_data_warehouse.duckdb # directory pointing to dw, under our project directory
      threads: 1

    prod:
      type: duckdb
      path: prod.duckdb
      threads: 4

────────────────────────────
📄 DBT Testing & Schema Validation  
────────────────────────────
This project uses DBT tests and schema YML files to validate the pipeline

✔️ Example test types:
- not_null: ensures required fields are present
- unique: enforces key uniqueness
- accepted_values: validates specific fields (e.g. job types)

✔️ Schema files:
- src_schema.yml
- dim_schema.yml

✔️ DBT SQL Tests:
- test_mart_duplicate_job_details.sql
- test_mart_no_duplicates.sql
-test_surrogate_key.sql

To run tests and validate your pipeline:

bash:
# Run the full pipeline
dbt build

# Or run step-by-step:
dbt run      # Runs models
dbt test     # Runs all schema + data tests

────────────────────────────
🧠 Gemini API Integration 
────────────────────────────
1. Get your API key from Google Gemini API Console:
https://ai.google.dev/gemini-api/docs/api-key

2. Create a .env file in your project root:

GEMINI_API_KEY=your-api-key-here

Make sure to exclude .env in .gitignore 

3. Your key is automatically loaded via python-dotenv

────────────────────────────
🖥️  Streamlit UI Features
────────────────────────────

This project includes a **Streamlit dashboard** for interactive exploration of job ad data and skill profiling using Gemini (Google's LLM).

Launch with:

bash
streamlit run app.py

────────────────────────────
 Contributors
────────────────────────────
Stefan Lundberg StefanLundberg77  
Susanna Rokka   SusannR11 
Richard Norrman richardnorrman  
Caroline Helmvee linehanna
