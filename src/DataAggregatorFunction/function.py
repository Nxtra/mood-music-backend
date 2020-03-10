import json
import boto3
import os
import pprint as pp


dynamodb = boto3.resource('dynamodb')
label_table = dynamodb.Table(os.environ['LABELLING_DYNAMODB_TABLE'])
features_table = dynamodb.Table(os.environ['FEATURES_DYNAMODB_TABLE'])
image_data_table = dynamodb.Table(os.environ["IMAGE_DATA_DYNAMODB_TABLE"])


def extract_dynamodb_image_data(data):
    print(json.dumps(data))
    image_id = data['Keys']['imageId']['S']
    author = data['Keys']['author']['S']
    uuid = data['NewImage']['uuid']['S']
    label = data['NewImage']['label']['S']
    return image_id, uuid, label, author


def handler(event, context):
    print("Executing")
    for record in event.get('Records'):
        image_id, uuid, label, author = extract_dynamodb_image_data(record['dynamodb'])
        image_key = image_id
        image_features = retrieve_image_features(image_key)
        print(image_features)
        assert image_features.get('imageId') == image_id
        aggregate_features_and_label_data(image_features, label, author, uuid)
#     merge features and label
#  save in result in database


def retrieve_image_features(image_key):
    response = features_table.get_item(Key={'imageId': image_key})
    return response.get('Item')


def aggregate_features_and_label_data(image_features, label, author, uuid):
    response = image_data_table.put_item(Item={
        'imageId': image_features.get('imageId'),
        'author': author,
        'uuid': uuid,
        'DISGUSTED': image_features.get('DISGUSTED'),
        'CONFUSED': image_features.get('CONFUSED'),
        'SURPRISED': image_features.get('SURPRISED'),
        'HAPPY': image_features.get('HAPPY'),
        'CALM': image_features.get('CALM'),
        'FEAR': image_features.get('FEAR'),
        'SAD': image_features.get('SAD'),
        'label': label
    })