# Set up orchestration of HiRe_Project pipeline.
# import Dagster packages


import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster_dlt import DagsterDltResource, dlt_assets

import dlt

from pathlib import Path

# data warehouse directory
db_path = str(Path(__file__).parents[1] / "ads_data_warehouse.duckdb")





