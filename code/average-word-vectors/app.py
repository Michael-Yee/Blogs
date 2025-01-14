import json

from utils import transform_data
from query import query_data


def average_word_vector(event, context):
    try:
        transform_data(event)

        body = {
            "message": "success"
        }

        return {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        body = {
            "message": "failed"
        }

        return {"statusCode": 400, "body": json.dumps(body)}


def query(event, context):
    try:
        query_data(event)

        return {"statusCode": 200, "body": json.dumps(event["body"])}
    except Exception as e:
        body = {
            "message": "failed"
        }

        return {"statusCode": 400, "body": json.dumps(body)}
