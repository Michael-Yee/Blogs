import ast
import json

import boto3
import botocore
from opensearchpy import OpenSearch

from inference import get_average_word_vector


def get_query_parameters(event):
    """Returns the query parameters """
    body_data = json.loads(event["body"])
    if "index" not in body_data:
        print("Missing index parameter")
        raise Exception("Missing index parameter")
    elif "keywords" not in body_data:
        print("Missing keywords parameter")
        raise Exception("Missing keywords parameter")

    index = body_data.get("index")
    size = body_data.get("size", 1)
    keywords = body_data.get("keywords")
    average_word_vector = get_average_word_vector(keywords)
    k = body_data.get("k", 3)

    return index, size, average_word_vector, k


def get_opensearch_client():
    """Creates and returns an OpenSearch client """
    host = "https://search-dev-us.aos.us-east-1.on.aws" #  TODO: Config file?
    ssm_client = boto3.client("ssm")
    auth = ssm_client.get_parameter(
        Name="/dev-us-opensearch/auth",
        WithDecryption=True
    )

    return OpenSearch(
        hosts=host,
        http_compress=True,
        http_auth=ast.literal_eval(auth["Parameter"]["Value"]),
        use_ssl=True,
        verify_certs=True,
    )


def opensearch_query(index, size, average_word_vector, k):
    """Returns the OpenSearch query response"""
    query = {
      "size": size,
      "query": {
        "knn": {
          "keywords_embedding": {
            "vector": average_word_vector,
            "k": k
          }
        }
      }
    }
    opensearch_client = get_opensearch_client()

    return opensearch_client.search(
        body = query,
        index = index
    )


def query_data(event):
    """Query data process steps"""
    index, size, average_word_vector, k = get_query_parameters(event)
    response = opensearch_query(index, size, average_word_vector, k)
    print(response) #  TODO: What should we do with the response?
