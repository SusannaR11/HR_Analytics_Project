# For
# instance, try to produce visualizations to answer these questions:
# for a specific occupation field (i.e. Data/IT), which occupation (i.e. data engineer) has a higher
# number of vacanies?
# which cities has a higher number of vacancies?
# etc
# You should include at least four meaningful KPI/metrics and visualizations on your dashboard that are able
# to improve efficiency of the work of talent acquisition specialists in this HR agency.

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly_express as px
from utilities.read_DB import AdsDB

# init db connection
db = AdsDB()


# Pie-chart function for top 10 number of vacancies/occupational role
def pie_occupation_grouped(df, top_n=10):

    
    # sort df and select top 10
    df_top = df.sort_values(by="num_vacancies",
                            ascending=False).head(top_n)


    fig = px.pie(df_top, names="occupation", values="num_vacancies",
                 title="Topp 10 vacancies per occupation")

    fig.update_traces(
    textinfo='percent',
    #hoverinfo='label+percent+value',
    textposition='inside',
    #insidetextorientation='radial',
    #pull=[0.05 if name == "Other" else 0 for name in df_combined["occupation"]]
)

#     fig.update_layout(
#     uniformtext_minsize=12,
#     uniformtext_mode='hide'
# )
    st.plotly_chart(fig, use_container_width=True)


# WTH hur många ads finns de??
# SKA MAN HA EN KPIS MED MASSA BRA GRUNDDATA?

def vacancies_per_locality():

    
    df = db.query("""SELECT
                  COUNT(vacancies) as count,
                  --SUM(vacancies) as sum,
                  --ANY_VALUE(workplace_region),
                  workplace_city as locality,
                  --ANY_VALUE(occupation)
                  FROM marts.mart_data_it
                  GROUP BY locality
                  ORDER BY count DESC
                  """)

    df_top = df.sort_values(by="count",
                            ascending=False).head(10)


    fig = px.bar(df_top, 
                 x= "locality",
                 y="count",
                 labels={"locality": "Stad", "count": "Antal tjänster"},
                 title="Vacancies per Locality top 10")
    #fig.show()
    st.plotly_chart(fig)

                 
    # f.vacancies,
    # f.relevance,
    # e.employer_name,
    # e.employer_workplace,
    # e.workplace_country,
    # e.workplace_region,
    # e.workplace_municipality,
    # o.occupation,
    # o.occupation_group,
    # o.occupation_field,
    # f.application_deadline,
    # jd.description,
    # jd.description_html,
    # jd.duration,
    # jd.salary_type,
    # jd.salary_description,
    # jd.working_hours_type