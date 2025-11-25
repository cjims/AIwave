import boto3
import json
import os

s3 = boto3.client('s3')
bucket_name = "testviedo"

def lambda_handler(event, context):
    # 取得 bucket 裡所有物件
    response = s3.list_objects_v2(Bucket=bucket_name)

    images = []
    
    for obj in response.get('Contents', []):
        key = obj['Key']
        # 如果是圖片檔
        if key.endswith((".png", ".jpg", ".jpeg", ".gif")):
            # 產生一個 presigned URL
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