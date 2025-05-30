import streamlit as st
import duckdb
from pathlib import Path
from streamlit_option_menu import option_menu
from utilities.read_DB import AdsDB
from visualisation.charts import pie_occupation, vacancies_per_locality

db = AdsDB()

# Connecting to the data warehouse
# db_path = Path(__file__).parent / "../ads_data_warehouse.duckdb"
# connection = duckdb.connect(database=str(db_path), read_only=True)

# Function for a dropdown menu to select different charts to see
def chart_dropdown_menu():
    selected_charts = st.multiselect(
        label='Charts',
        options=['Pie Chart', 'Spider Chart', 'Bar Chart']
    )

    if 'Pie Chart' in selected_charts:
        st.write("Pie Chart")
        # run pie-chart for top 10 occupations
        if selected == "Data/IT":
            pie_occupation()
            db.close() # method for closing

    if 'Spider Chart' in selected_charts:
        st.write("Spider Chart")

    if 'Bar Chart' in selected_charts:
        st.write("Bar Chart")
        if selected == "Data/IT":
            # run barchart for vacancies by city
            vacancies_per_locality() 
            db.close()

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
    chart_dropdown_menu()
if selected == "Yrken med social inriktning":
    st.title (f"{selected}")
    chart_dropdown_menu()
if selected == "Data/IT":
    st.title (f"{selected}")
    chart_dropdown_menu()

        
