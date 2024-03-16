import pandas as pd
import streamlit as st

from vagahertz_streamlit.gcloud_utils import *

st.set_page_config(page_title="Ottieni QR")

st.title('Ottieni QR')

storage_client = initialize_storage_client(store_json_key_from_env())
blobs = storage_client.list_blobs("vagahertz")

users_df = read_csv_from_gcs_private_bucket(
    storage_client,
    "vagahertz",
    "users_df.csv",
)


# user_email = st.text_input("Inserisci il tuo indirizzo email:")
# user_codice_fiscale = st.text_input("Inserisci il tuo codice fiscale")
#
# # button_check = st.button("Clicca per ottenere QR code")
#
# if True:
#     cols = st.columns((1, 1))
#     user_code = users_df.loc[users_df.codice_fiscale == user_codice_fiscale, "user_code"]
#     if user_email.lower() in users_df.email.str.lower().values and user_codice_fiscale in users_df.codice_fiscale.values:
#         user_code = users_df.loc[users_df.codice_fiscale == user_codice_fiscale, "user_code"].values[0]
#         user_real_name = users_df.loc[users_df.codice_fiscale == user_codice_fiscale, "nome"].values[0]
#         st.subheader("Ciao {}, ecco il tuo QR code per Non Solo Tekno!".format(user_real_name))
#         read_user_event_qrcode(
#             "vagahertz",
#             "events_access/non-solo-techno_2024-03-16/",
#             user_code + ".png",
#             storage_client
#         )
#     else:
#         st.warning("Questa coppia email-codicefiscale non è nel registro!")

nome = st.text_input("Inserisci il tuo indirizzo email:")
cognome = st.text_input("Inserisci il tuo codice fiscale")

# button_check = st.button("Clicca per ottenere QR code")

if True:
    cols = st.columns((1, 1))
    user_code = users_df.loc[users_df.codice_fiscale == user_codice_fiscale, "user_code"]
    if user_email.lower() in users_df.email.str.lower().values and user_codice_fiscale in users_df.codice_fiscale.values:
        user_code = users_df.loc[users_df.codice_fiscale == user_codice_fiscale, "user_code"].values[0]
        user_real_name = users_df.loc[users_df.codice_fiscale == user_codice_fiscale, "nome"].values[0]
        st.subheader("Ciao {}, ecco il tuo QR code per Non Solo Tekno!".format(user_real_name))
        read_user_event_qrcode(
            "vagahertz",
            "events_access/non-solo-techno_2024-03-16/",
            user_code + ".png",
            storage_client
        )
    else:
        st.warning("Questa coppia email-codicefiscale non è nel registro!")
