import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()


def generate_presigned_url(bucket_name, object_name, expiration=1800):
    """
    Generate a presigned URL for S3 object upload.

    :param bucket_name: Name of the S3 bucket.
    :param object_name: Key of the object in the bucket.
    :param expiration: Time in seconds for the presigned URL to remain valid.
    :return: Presigned URL as a string. If error, returns None.
    """
    s3_client = boto3.client('s3')

    try:
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': f"images/{object_name}",
                'ContentType': 'text/plain'
            },
            ExpiresIn=expiration
        )
        return presigned_url
    except NoCredentialsError:
        print("Credentials not available")
        return None


def main():
    # Load AWS credentials and S3 bucket information from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET')
    s3_bucket_name = os.getenv('AWS_BUCKET_NAME')
    aws_region = os.getenv('AWS_REGION')

    # Set AWS credentials and region
    boto3.setup_default_session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    # Example usage: generate a presigned URL for an object named 'example.txt'
    object_key = 'example.txt'
    presigned_url = generate_presigned_url(s3_bucket_name, object_key)

    if presigned_url:
        print(f"Presigned URL for upload: {presigned_url}")
    else:
        print("Failed to generate presigned URL.")


if __name__ == "__main__":
    main()
