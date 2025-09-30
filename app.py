import streamlit as st
import pandas as pd
import numpy as np
from multiagents import Agents4trends

import csv
import pandas as pd

# Read CSV with correct encoding (UTF-8 is usually best)
df = pd.read_csv("./FRurl_with_data2.csv", encoding="utf-8").fillna(value=0)

# Create lists and dictionary for lookup
List = []
requirements_dict = {}

with open("./FRurl_with_data2.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file, fieldnames=[
                            "Organization Website", "Scraped Titles"] + ["Scraped Description"])
    for row in reader:
        List.append(row['Organization Website'])
        # Store the mapping between ID and System Design Requirements
        requirements_dict[row['Organization Website']] = str(row["Scraped Titles"]) + " " + str(row['Scraped Description'])

st.set_page_config(
    page_title="My Streamlit App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header('Automating Company Classification Using AI')


options = st.multiselect(
    "What are THE company website you are intersed in ?",
    List,
    max_selections=1,
)


st.write("You selected:")

for selected_id in options:
    if selected_id in requirements_dict:
        st.write(
            f"**ID {selected_id,}:** {requirements_dict[selected_id]}")
        
        if st.button("Start classification"):
            company_analysis, trends_matcher , final_trend = Agents4trends(selected_id,requirements_dict[selected_id])
            tab1, tab2, tab3 = st.tabs(
                ["🧑‍💻 Company Analysis", "🤖 Potential trends", "🕵️ Final Trend"])

            with tab1:
                st.write(company_analysis)

            with tab2:
                st.write(trends_matcher)

            with tab3:
                st.write(final_trend)

