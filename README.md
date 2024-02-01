# S3 Image Generator
Create a SAM app that executes a Lambda that generates an image from the Bedrock Titan Image Generator G1 model, stores it in S3, then logs in CloudWatch.

You can generate the image using this command in the terminal with the AWS CLI:
`aws lambda invoke \
--function-name S3ImageGeneratorFunction \
--payload '{"text":"orange cat","seed":42}' \
--cli-binary-format raw-in-base64-out \
response.json`
