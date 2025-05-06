import streamlit as st
import duckdb
from pathlib import Path
from streamlit_option_menu import option_menu

# Connecting to the data warehouse
db_path = Path(__file__).parent / "ads_data_warehouse.duckdb"
connection = duckdb.connect(database=str(db_path), read_only=True)
