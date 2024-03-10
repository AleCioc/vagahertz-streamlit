import json

import pandas as pd
import streamlit as st

from vagahertz_streamlit.gcloud_utils import *


def read_json_files_in_folder(bucket_name, folder_name, json_key_path):
    """
    Reads all JSON files in a specified folder within a Google Cloud bucket,
    aggregates their contents into a list, and converts the list into a pandas DataFrame.

    :param bucket_name: Name of the Google Cloud bucket.
    :param folder_name: Folder name in the bucket to scan for JSON files.
    :param json_key_path: Path to the JSON key for GCloud authentication.
    :return: A pandas DataFrame containing the aggregated data from all JSON files.
    """
    # Initialize the storage client
    storage_client = initialize_storage_client(json_key_path)

    # List blobs in the specified folder
    blobs = list_blobs(bucket_name, folder_name, json_key_path)

    # Initialize an empty list to store data from all JSON files
    json_data_list = []

    # Download and read each JSON file, then append its content to the list
    for blob in blobs:
        if blob.name.endswith('.json'):
            # Define local file name
            local_file_name = blob.name.split('/')[-1]

            # Download the blob to a local file
            download_blob(storage_client, bucket_name, blob.name, local_file_name)

            # Read the JSON file and append its content to the list
            with open(local_file_name, 'r') as json_file:
                json_data = json.load(json_file)
                json_data_list.append(json_data)

            # Remove the file after processing
            os.remove(local_file_name)

    # Convert the list of JSON objects to a pandas DataFrame
    df = pd.DataFrame(json_data_list)
    return df


st.title('Visualizza utenti')

users_df = read_json_files_in_folder(
    "vagahertz",
    "unique_users_json/",
    os.path.join(root_data_path, "temp.json")
)
