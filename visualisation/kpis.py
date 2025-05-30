import streamlit as st
from utilities.read_DB import AdsDB

# init db connection
db = AdsDB()

def total_ads(df):

    # KPI
    df_total_ads = df["sum"].sum()
    st.metric(label="Totalt antal lediga tjänster", value=int(df_total_ads))

# query function for occupation    
def occupation_query():
             
    df_occupation = db.query("""
                        SELECT occupation as beteckning, 
                        sum(vacancies) AS antal
                        FROM mart.occupation_data_it
                        GROUP BY occupation
                        ORDER BY antal DESC""")
    return df_occupation

# query function for locality
def locality_query():
        
    df_location = db.query("""SELECT
                        SUM(vacancies) as sum,
                        occupation_field as field,
                        municipality as locality
                        FROM mart.occupation_data_it
                        GROUP BY locality, field
                        ORDER BY sum DESC
                        """)
    return df_location
