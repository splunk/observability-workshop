import requests
import streamlit as st  # type: ignore
from datetime import datetime
import pandas as pd
import json
from os import path
import yaml

year = datetime.now().year

VERSION = "1.9.0"
CAPTION = f"© {year} Splunk Inc. All rights reserved. **Version {VERSION}**"

st.set_page_config(
    page_title=f"Demo Client - Splunk",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
)

#st.image("images/splunk-logo-black-small.png")
st.caption(CAPTION)

if "auth_success" not in st.session_state:
    st.session_state.auth_success = False

st.session_state.valid_org = False

if not "valid_inputs_received" in st.session_state:
    st.session_state.valid_inputs_received = False

with st.form("demo_form") as form:
    host = st.text_input("Host", placeholder="hostname")
    port = st.text_input("Port", placeholder="8083", value="8083")
    query = st.selectbox("Query", ("pods", "health", "Deploy Online Boutique"))
    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        st.cache_data.clear()
        st.session_state.valid_inputs_received = True

if st.session_state.valid_inputs_received == False:
    st.warning(
        "TBD."
    )
else:
    
    if query == "pods":
        response = requests.get(f"http://{host}:{port}/{query}")
        df = pd.DataFrame.from_dict(response.json())
        st.dataframe(df)
    elif query == "health":
        response = requests.get(f"http://{host}:{port}/{query}")
        st.write(response.text)
    elif query == "Deploy Online Boutique":
        response = requests.get(f"http://{host}:{port}/apply_deployment")
        st.write(response.json())