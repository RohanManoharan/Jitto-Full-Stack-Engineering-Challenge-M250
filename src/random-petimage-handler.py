import json
import boto3
import base64
import random

s3 = boto3.client('s3')

def lambda_handler(event, context):

    try:
        # Get query params (label)
        query_params = event.get('queryStringParameters') or {}
        label = query_params.get('label')
        
        # Validate label
        if label not in ["cat", "dog"]:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f"Invalid pet type: {label}. Must be 'cat' or 'dog'"
                })
            }

        # Get bucket + contents
        bucket = "rm-petimagebucket"
        bucket_objects = s3.list_objects_v2(Bucket=bucket, Prefix=label)

        # If label doesn't have images in it
        if 'Contents' not in bucket_objects:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': f"No images found for pet type: {label}"
                })
            }
        
        # Filter files that  DONT end with / and add them to a list (this would prob never happen)
        files = []
        for obj in bucket_objects['Contents']:
            if not obj['Key'].endswith('/'):
                files.append(obj['Key'])
        
        # Get random file
        file_key = random.choice(files)
        
        # Gen presigned url for object
        presigned_url = s3.generate_presigned_url(
            'get_object',
             Params={'Bucket': bucket, 'Key': file_key},
              ExpiresIn=3600  # 1 hour
         )

        # Success msg    
        return {
            'statusCode': 200,
            'body': json.dumps({
                'image_url': presigned_url,
                'message': f'Here is your {label} image!',
                'expires_in': '1 hour'
            })
         }

    # For debugging purposes
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

