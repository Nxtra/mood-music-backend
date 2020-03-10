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

    if 'label' not in data or 'imageId' not in data or 'author' not in data:
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
    table = dynamodb.Table(os.environ['LABELLING_DYNAMODB_TABLE'])
    result = table.put_item(Item=item)
    print(result)


def make_item_to_save(data):
    timestamp = str(int(round(time.time() * 1000)))
    item = {
        'imageId': data['imageId'],
        'author': data['author'],
        'label': data['label'],
        'uuid': str(uuid.uuid4()),
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }
    return item
