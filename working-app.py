import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import duckdb
import numpy as np

#con = duckdb.connect("sgJobData.db")

print(f"🟢 Rerun at: {datetime.now()}")

#st.title("Hello, Streamlit! :wave:")
#st.write("This is my first Streamlit app.:smile:") 

#DATA_PATH="data/SGJobData.csv"
DATA_PATH="SGJobData_10000_random.csv"

# Sets the page configuration
# You can set the page title and layout here
st.set_page_config(page_title="SG Job dashboard", layout="wide")

#st.title("Singapore HDB Resale Dashboard")
#st.caption("Code-along: building a usable dashboard from real resale transactions.")

st.header("Dashboard Overview")
st.subheader("What this app will show")
st.markdown("""
- ###Transaction volume after filtering
- ###Average resale price
- ###Median floor area
- ###Town and flat type trends
""")

# df = pd.read_csv(DATA_PATH)
@st.cache_data
def load_data(path):
    print(f"🟠 Loading data at: {datetime.now()}")
    df = pd.read_csv(path)
    df["expiry_month"] = pd.to_datetime(df["metadata_expiryDate"])
    return df

df = load_data(DATA_PATH)

# First data display
st.write(f"Rows loaded: {len(df):,} | Columns: {len(df.columns)}")
#st.dataframe(df.head(20), width="stretch")

# Get unique values for towns and flat types
unique_employment_types = sorted(df["employmentTypes"].dropna().unique())
#unique_flat_types = sorted(df["flat_type"].dropna().unique())

# The code for the entire sidebar section looks like this:
st.sidebar.header("Filters")

# Create multi-selects for towns and flat types
selected_employment_types = st.sidebar.multiselect("Employment Type", unique_employment_types, default=[])
#selected_towns = st.multiselect("Town", unique_towns, default=[])
#selected_flat_types = st.sidebar.multiselect("Flat Type", unique_flat_types, default=[])


