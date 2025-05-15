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


# Pie-chart function for top 10 number of ads/occupational role
def pie_occupation_grouped(df, top_n=10):

    # sort df and select top 10
    df_top = df.sort_values(by="num_ads",
                            ascending=False).head(top_n)

    # count excessive ads data as other
    other_count = df["num_ads"].sum() - df_top["num_ads"].sum()
    if other_count > 0:
        df_other = pd.DataFrame([{
            "occupation": "Others",
            "num_ads": other_count
        }])
        df_combined = pd.concat([df_top, df_other], ignore_index=True)
    else:
        df_combined = df_top

    fig = px.pie(df_combined, names="occupation", values="num_ads",
                 title="Topp 10 ads per occupation")

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