import json
import logging
import boto3
from botocore.exceptions import ClientError
import base64

# This creates a logger instance
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# This initializes the clients Bedrock Runtime and S3
bedrock_runtime_client = boto3.client('bedrock-runtime', region_name='us-east-1')
s3 = boto3.client('s3')

bucket_name = 's3bucketname' # Add the s3 bucket you want to upload photos to

def lambda_handler(event, context):
    # We need to extract 'text' and 'seed' from the event, provide defaults if not present
    prompt = event.get('text', 'default prompt')
    seed = event.get('seed', 0)  # Default seed value if not provided

    try:
        base64_image_data = invoke_titan_image(prompt, seed)
        
        # The image data is a base64-encoded string, so we need to decode it to get the actual image data
        image_data = base64.b64decode(base64_image_data)
        object_key = f"generated_images/image_{prompt.replace(' ', '_')}_{seed}.jpg"

        # Now we upload the image data to S3
        s3.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=image_data,
            ContentType='image/jpeg'  # This is adjustable!
        )
        logger.info(f"Uploaded image to s3://{bucket_name}/{object_key}")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f"Image uploaded successfully to {bucket_name}/{object_key}."})
        }

    except Exception as e:
        logger.error("Error: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to invoke model or upload image', 'detail': str(e)})
        }

def invoke_titan_image(prompt, seed):
    try:
        request = json.dumps({
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {"text": prompt},
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "cfgScale": 8.0,
                "height": 512,
                "width": 512,
                "seed": seed,
            },
        })

        response = bedrock_runtime_client.invoke_model(
            modelId="amazon.titan-image-generator-v1", body=request
        )

        response_body = json.loads(response["body"].read())
        base64_image_data = response_body["images"][0]

        return base64_image_data

    except ClientError as e:
        logger.error(f"Couldn't invoke Titan Image generator: {e}")
        raise