import boto3
import os

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    bucket_name = 'testviedo-gen'
    key = event['queryStringParameters']['key']

    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': key},
        ExpiresIn=3600  # URL 有效時間，秒
    )

    return {
        'statusCode': 200,
        'headers': {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*"
        },
        'body': presigned_url
    }
