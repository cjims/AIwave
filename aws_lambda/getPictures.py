import boto3
import json
import os

s3 = boto3.client('s3')
bucket_name = "testviedo"

# 列出S3裡的圖片，產生presigned URL
def lambda_handler(event, context):
    response = s3.list_objects_v2(Bucket=bucket_name)

    images = []
    
    for obj in response.get('Contents', []):
        key = obj['Key']
        if key.endswith((".png", ".jpg", ".jpeg", ".gif")):
            # 產生presigned URL
            presigned_url = s3.generate_presigned_url('get_object',
                                                      Params={'Bucket': bucket_name, 'Key': key},
                                                      ExpiresIn=3600)
            images.append({
                "key": key,
                "url": presigned_url
            })

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*"
        },
        'body': json.dumps(images)
    }