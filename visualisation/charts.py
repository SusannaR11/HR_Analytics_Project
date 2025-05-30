# For
# instance, try to produce visualizations to answer these questions:
# for a specific occupation field (i.e. Data/IT), which occupation (i.e. data engineer) has a higher
# number of vacanies?
# which cities has a higher number of vacancies?
# etc
# You should include at least four meaningful KPI/metrics and visualizations on your dashboard that are able
# to improve efficiency of the work of talent acquisition specialists in this HR agency.

import streamlit as st
import plotly_express as px
from visualisation.kpis import occupation_query, locality_query, total_ads

# Pie-chart function vacancies/occupational role
def pie_occupation():

    df = occupation_query()

    top = st.checkbox("Visa top 10", value=False) 

    # check user input
    if top:
        # sort df and select top 10
        df_top = df.sort_values(by="antal",
                                ascending=False).head(10)
        df = df_top


    fig = px.pie(df, names="beteckning",
                         values="antal",
                         labels={"beteckning":"Beteckning", "antal":"Antal lediga tjänster"},
                         title="Lediga tjänster per yrkesbeteckning")

    fig.update_traces(
    textinfo='percent',
    hoverinfo='label+percent+value',
    textposition='inside')
    st.plotly_chart(fig, use_container_width=True)

def vacancies_per_locality():

    # create Dataframe from query
    df = locality_query()
    # header for chart
    st.subheader("Antal lediga tjänster per ort")

    # checkbox for missing city data
    missing_city_data = st.checkbox("Inkludera annonser där 'Stad ej angiven'", value=False) 

    # check user input
    if not missing_city_data:
        df = df[df["locality"] != "Ej angivet"]
    
    # Sort values after top 10
    df_top = df.sort_values(by="sum",
                            ascending=False).head(10)

    # create figure
    fig = px.bar(df_top, 
                 x="locality",
                 y="sum",
                 labels={"locality": "Stad", "sum": "Antal lediga tjänster"},
                 hover_name='field',
                 hover_data=[],
                 color='locality',
                 text_auto=True)
    #fig.show()
    st.plotly_chart(fig)

    # KPI
    total_ads(df_top)
