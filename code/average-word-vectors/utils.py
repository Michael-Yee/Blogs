from datetime import datetime
import json
import os
import urllib.parse
import uuid

import boto3
import botocore
import polars as pl
import gzip

from inference import get_average_word_vector


UPLOAD_BUCKET = "average-word-vector"
UPLOAD_KEY = "word_embeddings"
DOWNLOAD_PATH = f"/tmp/{uuid.uuid4()}.gz"
UPLOAD_PATH = f"/tmp/{uuid.uuid4()}.parquet"


def get_bucket_and_key(event):
    """Returns the bucket and key parsed from the event"""
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")

    return bucket, key


def key_exists(s3_client, bucket, key):
    """Returns a booleans if the bucket/key exists"""
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        print(f"{bucket}/{key} exist!")

        return True
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"{bucket}/{key} does not exist!")
            return False
        else:
            print(f"Something went wrong querying for {bucket}/{key} : {e}")
            raise


def my_custom_polars_function(keywords_embedding):
    """Returns a string representation of the average word vector for Text keyword values found in the keywords_embedding column"""
    jsonified = json.loads(keywords_embedding)
    if jsonified["Text"]:
        result = get_average_word_vector(jsonified["Text"])
    else:
        result = [0.0] * 300

    return result


def download_gzip(s3_client, bucket, key):
    """Downloads a gzip file from s3"""
    try:
        print(f"Downloading {bucket}/{key} to {DOWNLOAD_PATH}")
        response = s3_client.download_file(bucket, key, DOWNLOAD_PATH)
        print(f"Downloaded {bucket}/{key} as {DOWNLOAD_PATH}")
    except Exception as e:
        print(f"Something went wrong downloading from s3: '{e}'")
        raise


def transform_csv_data():
    """Removed unwanted columns and added a new column keywords_embedding with the string representation of the average word vector"""
    df = (
        pl.scan_csv(DOWNLOAD_PATH)
        # Select the columns we want
        .select("timestamp", "keywords")
        # Collect the data in chucks
        .collect(streaming=True)
    )

    # copy the keywords row data into a new keywords_embedding column
    df = df.with_columns(pl.col("keywords").alias("keywords_embedding"))
    # Replace the keywords_embedding row data with the average word vector
    df  = df.with_columns(pl.col("keywords_embedding").map_elements(my_custom_polars_function, return_dtype=pl.List(pl.Float32)))

    return df


def upload_parquet(s3_client, df, filename):
    """Uploads a parquet file to s3"""
    current_date= datetime.now().strftime("%Y-%m-%d")
    current_datetime_string = str(current_date)
    filename = f'{filename.split(".")[0]}.parquet'

    try:
        print(f"Saving data to file: {UPLOAD_PATH}")
        df.write_parquet(UPLOAD_PATH)
        print(f"Saved data to file: {UPLOAD_PATH}")
    except Exception as e:
        print(f"Something went saving file {UPLOAD_PATH}: {e}")
        raise

    try:
        print(f"Uploading {UPLOAD_PATH} to {UPLOAD_BUCKET}/{UPLOAD_KEY}/{current_datetime_string}/{filename}")
        response = s3_client.upload_file(UPLOAD_PATH, UPLOAD_BUCKET, f"{UPLOAD_KEY}/{current_datetime_string}/{filename}")
        print(f"Uploaded {UPLOAD_PATH} to {UPLOAD_BUCKET}/{UPLOAD_KEY}/{current_datetime_string}/{filename}")
    except Exception as e:
        print(f"Something went wrong uploading to s3: {e}")
        raise


def clean_up():
    """Delete temporary files"""
    try:
        print(f"Deleting files {DOWNLOAD_PATH} and {UPLOAD_PATH}")
        os.remove(DOWNLOAD_PATH)
        os.remove(UPLOAD_PATH)
        print(f"Deleted files {DOWNLOAD_PATH} and {UPLOAD_PATH}")
    except Exception as e:
        print(f"Something went wrong deleting files {DOWNLOAD_PATH} and {UPLOAD_PATH}: '{e}'")
        raise


def transform_data(event):
    """Transforming data process steps"""
    s3_client = boto3.client("s3")
    bucket, key = get_bucket_and_key(event)

    if key_exists(s3_client, bucket, key):
        if key.endswith(".csv"):
            pass
        elif key.endswith(".gz"):
            print("Processing file")
            download_gzip(s3_client, bucket, key)
            df = transform_csv_data()
            upload_parquet(s3_client, df, key)
            clean_up()
            print("Processed file")
        else:
            print("Error!")
