import pandas as pd

from vagahertz_streamlit.gcloud_utils import *

st.set_page_config(page_title="Controlla accesso")

st.title('Controllo Accessi')

storage_client = initialize_storage_client(store_json_key_from_env())
blobs = storage_client.list_blobs("vagahertz")

blobs = list_blobs("vagahertz", "unique_users_json", storage_client)

users_df = read_json_files_in_folder(
    "vagahertz",
    "unique_users_json",
    storage_client
)

st.subheader("Lista tessere")
with st.expander("Clicca per visualizzare le tessere registrate"):
    users_df

storage_client = initialize_storage_client(store_json_key_from_env())
blobs = storage_client.list_blobs("vagahertz")

blobs = list_blobs(
    "vagahertz",
    "events_access/non-solo-techno_2024-03-16/",
    storage_client
)

event_users_df = read_json_files_in_folder(
    "vagahertz",
    "events_access/non-solo-techno_2024-03-16/",
    storage_client
)
if not len(event_users_df):
    event_users_df = pd.DataFrame(columns=["user_code"])

st.subheader("Lista ingressi effettuati")
with st.expander("Clicca per visualizzare chi è già entrat*"):
    event_users_df

if "user_code" not in st.query_params:
    st.warning("Inserisci un codice utente nell' URL per verificare l'accesso")
else:
    st.subheader("Verifica accesso per " + st.query_params["user_code"])
    if st.query_params["user_code"] in users_df.user_code.values:
        if st.query_params["user_code"] not in event_users_df.user_code.values:
            with open(os.path.join(root_data_path, "check_" + st.query_params["user_code"] + ".json"), "w") as f:
                json.dump({"user_code": st.query_params["user_code"]}, f)
            upload_blob(
                "vagahertz",
                os.path.join(root_data_path, "check_" + st.query_params["user_code"] + ".json"),
                "events_access/non-solo-techno_2024-03-16/" + st.query_params["user_code"] + ".json",
                storage_client
            )
            st.success("Ingresso consentito con questa tessera!")
        else:
            st.error("Ingresso già effettuato con questa tessera!")
    else:
        st.error("Tessera non registrata!")
