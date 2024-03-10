import os
from google.cloud import storage

from vagahertz_streamlit.path_config import *


def store_json_key_from_env():
    """
    Reads the JSON key from the 'JSON_KEY_GCLOUD' environment variable and writes it to a file
    specified by the 'JSON_KEY_PATH' environment variable.
    """
    json_key = os.getenv('JSON_KEY_GCLOUD').replace('\"', '"')
    if not json_key:
        raise ValueError("Environment variable 'JSON_KEY_GCLOUD' is not set.")

    json_key_path = os.getenv('JSON_KEY_PATH')
    if not json_key_path:
        raise ValueError("Environment variable 'JSON_KEY_PATH' is not set.")

    json_key_path = os.path.join(root_data_path, json_key_path)

    # Writing the JSON key to the specified file path
    with open(json_key_path, 'w') as json_file:
        json_file.write(json_key)

    # print(f"JSON key is stored at {json_key_path}.")

    return json_key_path


def initialize_storage_client(json_key_path):
    storage_client = storage.Client.from_service_account_json(json_key_path)
    return storage_client


def list_blobs(bucket_name, storage_client):
    """
    Lists all the blobs in the specified bucket.

    :param bucket_name: The name of the bucket.
    :param storage_client: The GCloud storage client
    """

    blobs = storage_client.list_blobs(bucket_name)

    blob_names = [blob.name for blob in blobs]

    return blob_names


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
