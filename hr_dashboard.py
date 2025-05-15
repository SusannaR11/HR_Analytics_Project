import streamlit as st
from streamlit_option_menu import option_menu
from utilities.read_DB import AdsDB
from visualisation.charts import pie_occupation_grouped

db = AdsDB()

# Connecting to the data warehouse
# db_path = Path(__file__).parent / "ads_data_warehouse.duckdb"
# connection = duckdb.connect(database=str(db_path), read_only=True)

# Function for a dropdown menu to select different charts to see
def chart_dropdown_menu():
    selected_charts = st.multiselect(
        label='Charts',
        options=['Pie Chart', 'Spider Chart', 'Bar Chart']
    )

    if 'Pie Chart' in selected_charts:
        st.write("Pie Chart")

    if 'Spider Chart' in selected_charts:
        st.write("Spider Chart")

    if 'Bar Chart' in selected_charts:
        st.write("Bar Chart")

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
    
    # pie_chart ads per occupation role
    df_occupation = db.query("""
    SELECT occupation, COUNT(*) AS num_ads
    FROM mart_data_it
    GROUP BY occupation
    ORDER BY num_ads DESC
    """)
    pie_occupation_grouped(df_occupation)
