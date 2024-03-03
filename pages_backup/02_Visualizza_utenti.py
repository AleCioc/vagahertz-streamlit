import json
import os

import pandas as pd
import streamlit as st
from vagahertz_streamlit.path_config import *

st.title('Visualizza utenti')

user_records_list = list()
for user_info_file in os.listdir(unique_users_json_path):
    if user_info_file.endswith(".json"):
        with open(os.path.join(unique_users_json_path, user_info_file), "r") as f:
            user_info_record = json.load(f)
            user_records_list.append(user_info_record)

st.dataframe(pd.DataFrame(user_records_list))
