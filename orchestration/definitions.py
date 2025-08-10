# Set up orchestration of HiRe_Project pipeline. Create a asset-based setup
# to enable tracking of historical patterns and monitor updates
# import Dagster packages

import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster_dlt import DagsterDltResource, dlt_assets
from pathlib import Path
import dlt
from load_api import (jobads_source_data_it, jobads_source_security, jobads_source_social)
from datetime import datetime
import json
import duckdb
from dagster import multiprocess_executor 

summary_path = Path(__file__).parents[1] / "job_update_summary.json"

# import Dagster wrapper source
import sys
sys.path.insert(0, str(Path(__file__).parents[1])) #points at project root

# Paths to duckdb warehouse and dbt
db_path = str(Path(__file__).parents[1] / "ads_data_warehouse.duckdb")
dbt_project_directory = Path(__file__).parents[1] / "dbt_code"
profiles_dir = Path.home() / ".dbt"

# dlt resource
dlt_resource = DagsterDltResource()
dbt_resource = DbtCliResource(project_dir=dbt_project_directory, profiles_dir=profiles_dir)


# dlt assets for 3 occupation fields
# Data / IT dlt Asset
@dlt_assets(
    dlt_source=jobads_source_data_it(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="jobads_data_it",
        dataset_name="staging",
        destination=dlt.destinations.duckdb(db_path),
    ),
)
def dlt_load_data_it(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(
        context=context)

# Socialt arbete dlt Asset
@dlt_assets(
    dlt_source=jobads_source_social(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="jobads_social",
        dataset_name="staging",
        destination=dlt.destinations.duckdb(db_path),
    ),
)
def dlt_load_social(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(
        context=context)

# Säkerhet och bevakning dlt Asset
@dlt_assets(
    dlt_source=jobads_source_security(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="jobads_security",
        dataset_name="staging",
        destination=dlt.destinations.duckdb(db_path),
    ),
)
def dlt_load_security(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(
         context=context)

# dbt Asset
dbt_project = DbtProject(project_dir=dbt_project_directory, profiles_dir=profiles_dir)
#dbt_project.prepare_if_dev()

# Asset for running 'dbt build'
@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

# Asset for logging update
@dg.asset(deps=[dlt_load_data_it, dlt_load_social, dlt_load_security, dbt_models])
def write_update_summary(context: dg.AssetExecutionContext):
#read current total from mart tables for calculating daily new jobs
    con=duckdb.connect(database=db_path, read_only=True)
    totals = {
        "Data/IT": con.execute("SELECT COUNT(*) FROM mart.occupation_data_it").fetchone()[0],
        "Säkerhet och bevakning": con.execute("SELECT COUNT(*) FROM mart.occupation_sakerhet_bevakning").fetchone()[0],
        "Yrken med social inriktning": con.execute("SELECT COUNT(*) FROM mart.occupation_socialt_arbete").fetchone()[0],
    }
    con.close()
# load previous total
    prev_totals = {}
    if summary_path.exists():
        try:
            with open(summary_path, "r", encoding="utf-8") as f:
                prev_totals = (json.load(f) or {}).get("totals", {})
        except Exception:
            prev_totals = {}

    new_today = {k: max(int(totals[k]) - int(prev_totals.get(k, 0)), 0) for k in totals}

# 3) Write summary JSON used by Streamlit
    payload = {
        "status": "success",
        "updated_at": datetime.now().isoformat(),
        "run_id": context.run_id,
        "totals": totals,
        "new_today": new_today,
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

# Jobs
job_api = dg.define_asset_job(
    "job_api",
    selection=dg.AssetSelection.keys(
        "dlt_jobads_source_data_it_jobsearch_resource",
        "dlt_jobads_source_social_jobsearch_resource",
        "dlt_jobads_source_security_jobsearch_resource",
    ),
    executor_def=multiprocess_executor.configured({"max_concurrent": 1}), # so that the 3 jobs don't get written at the same time. causes error
)

job_dbt = dg.define_asset_job(
    "job_dbt", 
    selection=dg.AssetSelection.keys(
        ["mart", "occupation_data_it"],
        ["mart", "occupation_sakerhet_bevakning"],
        ["mart", "occupation_socialt_arbete"],
        )
        | dg.AssetSelection.keys("write_update_summary") # runs logger asset
)

job_track = dg.define_asset_job(
    "job_track",
    selection=dg.AssetSelection.keys(
        "dlt_jobads_source_data_it_jobsearch_resource",
        "dlt_jobads_source_social_jobsearch_resource",
        "dlt_jobads_source_security_jobsearch_resource",
    )
)

# Schedule
# API path refresh daily
schedule_api = dg.ScheduleDefinition(
    job=job_api,
    #cron_schedule="00 05 * * *"  #Daily at 5:00 UTC ie 7:00 UTC+2 (Swedish summer time)
    cron_schedule="*/5 * * * *" #every 5 minutes
)

# Sensors
# if API refreshes succesfully, sensors will trigger to dbt build and 
# monitor each occupation field daily for new jobs

@dg.run_status_sensor(run_status=dg.DagsterRunStatus.SUCCESS, monitored_jobs=[job_api], name="api_success_sensor")
def api_success_sensor(context):
    yield dg.RunRequest(job_name="job_dbt")

@dg.run_status_sensor(run_status=dg.DagsterRunStatus.SUCCESS, monitored_jobs=[job_dbt], name="dbt_success_sensor")
def dbt_success_sensor(context):
    yield dg.RunRequest(job_name="job_track")

#log failure:
def _write_failed_summary(run_id: str, note:str):
    payload = {
        "status": "failed",
        "updated_at": datetime.now().isoformat(),
        "run_id": run_id,
        "note": note,
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

@dg.run_status_sensor(run_status=dg.DagsterRunStatus.FAILURE, monitored_jobs=[job_api], name="api_failed_sensor")
def api_failed_sensor(context, dagster_run):
    _write_failed_summary(dagster_run.run_id, "API stage failed")

@dg.run_status_sensor(run_status=dg.DagsterRunStatus.FAILURE, monitored_jobs=[job_dbt], name="dbt_failed_sensor")
def dbt_failed_sensor(context, dagster_run):
    _write_failed_summary(dagster_run.run_id, "DBT stage failed")

#Definitions 

defs = dg.Definitions(
    assets=[dlt_load_data_it, dlt_load_social, dlt_load_security, dbt_models, write_update_summary],
    resources={"dlt": dlt_resource, "dbt": dbt_resource},
    jobs=[job_api, job_dbt, job_track],
    schedules=[schedule_api],
    sensors=[api_success_sensor, dbt_success_sensor, api_failed_sensor, dbt_failed_sensor],
)


# Deploy Dagster UI using command:
# dagster dev -f orchestration/definitions.py from project root folder



