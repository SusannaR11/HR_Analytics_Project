# Set up orchestration of HiRe_Project pipeline. Create a asset-based setup
# to enable tracking of historical patterns and monitor updates
# import Dagster packages


import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster_dlt import DagsterDltResource, dlt_assets
from pathlib import Path
import dlt
from load_api import jobads_source_data_it, jobads_source_sakerhet_bevakning, jobads_source_socialt_arbete

# import Dagsater wrapper source
import sys
sys.path.insert(0, str(Path(__file__).parents[0])) #points at project root
from load_api import jobads_source

# Paths to duckdb warehouse and dbt
db_path = str(Path(__file__).parents[1] / "ads_data_warehouse.duckdb")
dbt_project_directory = Path(__file__).parent / "dbt_code"
profiles_dir = Path.home() / ".dbt"

# dlt resource
dlt_resource = DagsterDltResource()
dbt_resource = DbtCliResource(project_dir=dbt_project_directory, profiles_dir=profiles_dir)


# dlt assets for 3 occupation fields
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
    
# dbt resource
dbt_project = DbtProject(project_dir=dbt_project_directory, profiles_dir=profiles_dir)
dbt_project.prepare_if_dev()

@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

# Jobs
job_dlt = dg.define_asset_job("job_dlt", selection=dg.AssetSelection.keys("dlt_jobads_source_jobsearch_resource"))
job_dbt = dg.define_asset_job("job_dbt", selection=dg.AssetSelection.keys("occupation_socialt_arbete"))

# Schedule
schedule_dlt = dg.ScheduleDefinition(
    job=job_dlt,
    cron_schedule="9 00 * * *" 
)




