import streamlit as st
import duckdb
from pathlib import Path
from streamlit_option_menu import option_menu

# Connecting to the data warehouse
db_path = Path(__file__).parent / "ads_data_warehouse.duckdb"
connection = duckdb.connect(database=str(db_path), read_only=True)

# Sidebar for different options
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Säkerhet och bevakning", "Yrken med social inriktning", "Data/IT"],
        icons=["house", "fingerprint", "person-arms-up", "pc-display-horizontal"],
        default_index=0
    )

# Changing "page" based on selected option
if selected == "Home":
    st.title (f"{selected}")
if selected == "Säkerhet och bevakning":
    st.title (f"{selected}")
if selected == "Yrken med social inriktning":
    st.title (f"{selected}")
if selected == "Data/IT":
    st.title (f"{selected}")