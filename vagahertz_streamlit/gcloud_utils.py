import json
import os
import streamlit as st
import pandas as pd
from google.cloud import storage

from vagahertz_streamlit.path_config import *

st.set_page_config('VagaHertz', initial_sidebar_state='collapsed')


def store_json_key_from_env():
    """
    Reads the JSON key from the 'JSON_KEY_GCLOUD' environment variable and writes it to a file
    specified by the 'JSON_KEY_PATH' environment variable.
    """
    try:
        json_key = dict(st.secrets['JSON_KEY_GCLOUD'])
        for k in json_key:
            json_key[k] = json_key[k].replace("https=", "https:")
    except:
        json_key = os.getenv('JSON_KEY_GCLOUD')

    if not json_key:
        raise ValueError("Environment variable 'JSON_KEY_GCLOUD' is not set.")

    try:
        json_key_path = st.secrets['JSON_KEY_PATH']
    except:
        json_key_path = os.getenv('JSON_KEY_PATH')

    if not json_key_path:
        raise ValueError("Environment variable 'JSON_KEY_PATH' is not set.")

    json_key_path = os.path.join(root_data_path, json_key_path)

    # Writing the JSON key to the specified file path
    with open(json_key_path, 'w') as json_file:
        json.dump(json_key, json_file)

    # print(f"JSON key is stored at {json_key_path}.")

    return json_key_path


def initialize_storage_client(json_key_path):
    storage_client = storage.Client.from_service_account_json(json_key_path)
    return storage_client


def list_blobs(bucket_name, prefix, storage_client):
    """
    Lists all the blobs in the specified bucket.

    :param bucket_name: The name of the bucket.
    :param storage_client: The GCloud storage client
    """

    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
    return blobs


def download_blob(bucket_name, source_blob_name, destination_file_name, storage_client):
    """
    Downloads a blob from the bucket.

    :param bucket_name: The name of the bucket.
    :param source_blob_name: The name of the blob to download.
    :param destination_file_name: The local path to which the file should be downloaded.
    :param storage_client: The GCloud storage client
    """
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)
    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")


def upload_blob(bucket_name, source_file_name, destination_blob_name, storage_client):
    """
    Uploads a file to the bucket.

    :param bucket_name: The name of the bucket.
    :param source_file_name: The local path of the file to upload.
    :param destination_blob_name: The name of the blob.
    :param storage_client: The GCloud storage client
    """
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def read_json_files_in_folder(bucket_name, folder_name, storage_client):
    """
    Reads all JSON files in a specified folder within a Google Cloud bucket,
    aggregates their contents into a list, and converts the list into a pandas DataFrame.

    :param bucket_name: Name of the Google Cloud bucket.
    :param folder_name: Folder name in the bucket to scan for JSON files.
    :param json_key_path: Path to the JSON key for GCloud authentication.
    :return: A pandas DataFrame containing the aggregated data from all JSON files.
    """

    # List blobs in the specified folder
    blobs = list_blobs(bucket_name, folder_name, storage_client)

    # Initialize an empty list to store data from all JSON files
    json_data_list = []

    # Download and read each JSON file, then append its content to the list
    for blob in blobs:
        if blob.name.endswith('.json'):
            # Define local file name
            local_file_path = os.path.join(root_data_path, "temp.json")

            # Download the blob to a local file
            download_blob(bucket_name, blob.name, local_file_path, storage_client)

            # Read the JSON file and append its content to the list
            with open(local_file_path, 'r') as json_file:
                json_data = json.load(json_file)
                json_data_list.append(json_data)

            # Remove the file after processing
            os.remove(local_file_path)

    # Convert the list of JSON objects to a pandas DataFrame
    df = pd.DataFrame(json_data_list)
    return df
