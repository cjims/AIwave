import boto3
import json
import time
import io
import subprocess

kvs_client = boto3.client('kinesisvideo')
s3_client = boto3.client('s3')

STREAM_NAME = 'designvideo'
BUCKET_NAME = 'kvsstream'

def convert_to_mp4(input_file, output_file):
    """將TS格式的視頻轉換為MP4格式"""
    try:
        subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', output_file])
        print(f"Video successfully converted to {output_file}")
    except Exception as e:
        print(f"Error during conversion: {e}")

def lambda_handler(event, context):
    print(f"Received event: {event}")

    if not STREAM_NAME or not BUCKET_NAME:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing STREAM_NAME or BUCKET_NAME.')
        }

    try:
        # Step 1: Get data endpoint
        endpoint_response = kvs_client.get_data_endpoint(
            StreamName=STREAM_NAME,
            APIName='GET_MEDIA'
        )
        endpoint = endpoint_response['DataEndpoint']
        print(f"Data endpoint: {endpoint}")

        # Step 2: Initialize media client
        kvs_media_client = boto3.client('kinesis-video-media', endpoint_url=endpoint)

        # Step 3: Get media
        media_response = kvs_media_client.get_media(
            StreamName=STREAM_NAME,
            StartSelector={'StartSelectorType': 'NOW'}
        )

        payload_stream = media_response['Payload']

        # Step 4: Read payload for 40 seconds and write it to buffer
        buffer = io.BytesIO()
        start_time = time.time()
        max_duration_seconds = 40

        while time.time() - start_time < max_duration_seconds:
            chunk = payload_stream.read(4096)  # Read 4KB at a time
            if not chunk:
                break  # Stream ended
            buffer.write(chunk)

        if buffer.tell() > 0:
            buffer.seek(0)
            timestamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
            ts_key = f"{STREAM_NAME}/{timestamp}.ts"  # 使用TS格式儲存
            local_ts_file = f"/tmp/{timestamp}.ts"

            # Step 5: Save the buffer to a local file
            with open(local_ts_file, 'wb') as f:
                f.write(buffer.getvalue())
            print(f"Saved raw video as {local_ts_file}")

            # Step 6: Convert TS to MP4 using FFmpeg
            mp4_file = f"/tmp/{timestamp}.mp4"
            convert_to_mp4(local_ts_file, mp4_file)

            # Step 7: Upload converted video to S3
            with open(mp4_file, 'rb') as f:
                s3_client.upload_fileobj(f, BUCKET_NAME, f"{STREAM_NAME}/{timestamp}.mp4")

            print(f"Successfully stored converted video to s3://{BUCKET_NAME}/{timestamp}.mp4")
            return {
                'statusCode': 200,
                'body': json.dumps(f'Successfully stored converted video to s3://{BUCKET_NAME}/{timestamp}.mp4')
            }
        else:
            print("No payload received.")
            return {
                'statusCode': 200,
                'body': json.dumps('No payload received.')
            }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
