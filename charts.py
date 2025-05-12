# For
# instance, try to produce visualizations to answer these questions:
# for a specific occupation field (i.e. Data/IT), which occupation (i.e. data engineer) has a higher
# number of vacanies?
# which cities has a higher number of vacancies?
# etc
# You should include at least four meaningful KPI/metrics and visualizations on your dashboard that are able
# to improve efficiency of the work of talent acquisition specialists in this HR agency.

import duckdb
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly_express as px
import duckdb
from utilities.read_DB import AdsDB

db = AdsDB()



