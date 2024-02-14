# S3 Image Generator

This SAM app demonstrates how to use AWS Lambda to make calls to Bedrock's Titan Image Generator G1, generate an image based on text input, upload those images into an S3 bucket, and log everything in CloudWatch.

## Setup

- [AWS CLI](https://aws.amazon.com/cli/) installed and configured
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) installed
- [Access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) to Bedrock Titan Image Generator G1 and permissions to create Lambda functions, API Gateway, and S3 buckets

### 1. Create a S3 Bucket

Create a S3 bucket where the generated images will be stored:

```bash
aws s3 mb s3://<YOUR_BUCKET_NAME> --region <YOUR_REGION>
```
Clone this repo and update the `template.yaml` and `app.py` with your S3 bucket.

### 2. Deploy your SAM app
```bash
sam build
```
And then deploy your app to your account:

```bash
sam deploy
```

### 3. Test by invoking the Lambda locally

You can run this CLI command to invoke the Lambda and check the generated `response.json` to see if an image was successfully made and stored:

``` bash
aws lambda invoke \
--function-name <YOUR_FUNCTION_NAME> \
--payload '{"text":"Add image prompt here","seed":42}' \
response.json
```

Of course, CloudWatch should capture this entire invocation too. Can read more about my experience building this [here](https://community.aws/content/2byFjF8W1HHkzgis1aJokbXAJ6t/generate-and-store-images-in).
