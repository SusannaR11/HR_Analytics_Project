# Set up orchestration of HiRe_Project pipeline. Create a asset-based setup
# to enable tracking of historical patterns and monitor updates
# import Dagster packages


import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster_dlt import DagsterDltResource, dlt_assets
from pathlib import Path
import dlt
from load_api import (jobads_source_data_it, jobads_source_sakerhet_bevakning, jobads_source_socialt_arbete)

# import Dagsater wrapper source
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
    yield from dlt.run(context=context)

# Socialt arbete dlt Asset
@dlt_assets(
    dlt_source=jobads_source_socialt_arbete(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="jobads_social",
        dataset_name="staging",
        destination=dlt.destinations.duckdb(db_path),
    ),
)
def dlt_load_social(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

# Säkerhet och bevakning dlt Asset
@dlt_assets(
    dlt_source=jobads_source_sakerhet_bevakning(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="jobads_security",
        dataset_name="staging",
        destination=dlt.destinations.duckdb(db_path),
    ),
)
def dlt_load_security(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

# dbt Asset
dbt_project = DbtProject(project_dir=dbt_project_directory, profiles_dir=profiles_dir)
#dbt_project.prepare_if_dev()

# Asset for running 'dbt build'
@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

# Jobs
job_api = dg.define_asset_job(
    "job_api",
    selection=dg.AssetSelection.keys(
        "dlt_jobads_source_data_it_jobsearch_resource",
        "dlt_jobads_source_social_jobsearch_resource",
        "dlt_jobads_source_security_jobsearch_resource",
    )
)

job_dbt = dg.define_asset_job(
    "job_dbt", 
    selection=dg.AssetSelection.keys(
        "occupation_data_it",
        "occupation_sakerhet_bevakning",
        "occupation_socialt_arbete"
        )
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
    cron_schedule="7 00 * * *"  #Daily at 7:00 UTC ie 9:00 ECT
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

#Definitions 

defs = dg.Definitions(
    assets=[dlt_load_data_it, dlt_load_social, dlt_load_security, dbt_models],
    resources={"dlt": dlt_resource, "dbt": dbt_resource},
    jobs=[job_api, job_dbt, job_track],
    schedules=[schedule_api],
    sensors=[api_success_sensor, dbt_success_sensor],
)


# Deploy Dagster UI using command:
# dagster dev -f orchestration/definitions.py from project root folder



