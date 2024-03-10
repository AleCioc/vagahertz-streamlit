from vagahertz_streamlit.gcloud_utils import *


st.title('Visualizza utenti')

storage_client = initialize_storage_client(store_json_key_from_env())
blobs = storage_client.list_blobs("vagahertz")

blobs = list_blobs("vagahertz", "unique_users_json", storage_client)

users_df = read_json_files_in_folder(
    "vagahertz",
    "unique_users_json",
    storage_client
)

users_df
