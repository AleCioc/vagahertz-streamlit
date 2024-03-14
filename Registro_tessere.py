from vagahertz_streamlit.gcloud_utils import *

st.set_page_config(page_title="Registro tessere")

st.title('Registro tessere')

storage_client = initialize_storage_client(store_json_key_from_env())
blobs = storage_client.list_blobs("vagahertz")

blobs = list_blobs("vagahertz", "unique_users_json", storage_client)

users_df = read_json_files_in_folder(
    "vagahertz",
    "unique_users_json",
    storage_client
)

with st.expander("Guarda registro completo"):
    users_df

st.header("Pagamento tessera")


st.header("Non Solo Techno")

storage_client = initialize_storage_client(store_json_key_from_env())
blobs = storage_client.list_blobs("vagahertz")

blobs = list_blobs(
    "vagahertz",
    "events_access/non-solo-techno_2024-03-16/",
    storage_client
)

users_df = read_json_files_in_folder(
    "vagahertz",
    "events_access/non-solo-techno_2024-03-16/",
    storage_client
)
if not len(users_df):
    users_df = pd.DataFrame(columns=["user_code"])

st.subheader("Lista ingressi")
with st.expander("Clicca per visualizzare ingressi"):
    users_df
