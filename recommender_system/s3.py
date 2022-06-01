from dotenv import load_dotenv
import os
import boto3
import json
import pandas as pd

load_dotenv()

s3 = boto3.resource('s3',
                    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'))

def get_json_from_s3(bucket, key):
    obj = s3.Object(bucket, key)
    data = obj.get()['Body'].read().decode('utf-8')
    data = json.loads(data)
    return data

def get_dataframe_from_s3(bucket, key):
    obj = s3.Object(bucket, key)
    data = obj.get()['Body']
    df = pd.read_pickle(data)
    return df

def put_data_to_s3(bucket, key, data):
    obj = s3.Object(bucket, key)
    response = obj.put(Body=data)
    return response