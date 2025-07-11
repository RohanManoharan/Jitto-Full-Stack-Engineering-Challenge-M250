import json
import boto3
import base64
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:

        # Extract headers from API Gateway event
        headers = event.get('headers')
        
        #TODO: can possibly optimize this by turning it into an if statement?
        # Get metadata headers (Content-Type + Pet)
        metadata = {}
        for key, value in headers.items():
            if key.lower().startswith('x-amz-meta-'):
                meta_key = key[11:]  # Remove 'x-amz-meta-' prefix
                metadata[meta_key] = value

        # Get content type
        content_type = ''
        for key, value in headers.items():
            if key.lower() == 'content-type':
                content_type = value.lower()
                break       
        
        # Validate pet metadata before uploading
        pet_value = metadata.get('pet')
        if pet_value not in ['dog', 'cat']:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f"Invalid pet type: {pet_value}. Must be 'cat' or 'dog'"
                })
            } 

        # Map allowed content types to file extensions
        content_type_mapping = {
            'image/jpeg': '.jpg',
            'image/jpg': '.jpg',
            'image/png': '.png',
            'image/webp': '.webp'
        }
        
        # Check for valid content type
        if content_type not in content_type_mapping:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f"Invalid file type: {content_type}. Must be image/jpeg, image/png, or image/webp"
                })
            }
        
        # Get file extension
        file_extension = content_type_mapping[content_type]
        
        # Get the file content from the request body
        body = event.get('body')
        if event.get('isBase64Encoded', False):
            body = base64.b64decode(body)

        # Upload to /cat or /dog folder
        if pet_value == 'cat':
            key = f"cat/{context.aws_request_id}{file_extension}"
        else:
            key = f"dog/{context.aws_request_id}{file_extension}"
        
        # Upload to S3
        s3.put_object(
            Bucket='rm-petimagebucket',
            Key=key,
            Body=body,
            ContentType=content_type,
            Metadata=metadata
        )
        
        # Success msg
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Upload Successfull!',
                'key': key,
                'pet': pet_value,
                'file_type': content_type
            })
        }

    # For debugging purposes
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
