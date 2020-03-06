import json
import logging
import os
import time
import uuid
from datetime import datetime

import boto3

dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    data = json.loads(event['body'])

    if 'label' not in data or 'imageId' not in data:
        logging.error("Validation Failed")
        response_body = {
            "message": "Missing required fields"
        }
        response = {
            "statusCode": 404,
            "body": json.dumps(response_body)
        }
        return response

    item = make_item_to_save(data)

    save_item(item)

    response = {
        "statusCode": 201,
        "body": json.dumps(item)
    }

    return response


def save_item(item):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    table.put_item(Item=item)


def make_item_to_save(data):
    timestamp = str(int(round(time.time() * 1000)))
    item = {
        'imageId': data['imageId'],
        'uuid': str(uuid.uuid4()),
        'label': data['label'],
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    return item