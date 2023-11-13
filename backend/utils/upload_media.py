import uuid
from db import crud, enums
import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()

seperator = "$$$"
IMG_TIMEOUT = 1800


def init_aws_client():
    # Load AWS credentials and S3 bucket information from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET')
    aws_region = os.getenv('AWS_REGION')

    # Set AWS credentials and region
    boto3.setup_default_session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )


def generate_image_presigned_url(image_name: str, email: str, content_id: int, db):
    valid_extensions = ['jpeg', 'jpg', 'png', 'gif']
    file_extension = image_name.split('.')[-1].lower()

    if file_extension not in valid_extensions:
        print("")
        return None

    if file_extension == 'jpg':
        file_extension = 'jpeg'

    # append UUID to image name
    uuid_value = uuid.uuid4()
    key_name = f"images/{uuid_value}/{image_name}"

    # save the entry in db with pending status
    crud.add_image(content_id, key_name, email, db)

    # init AWS client
    init_aws_client()

    # create AWS stuff
    s3_client = boto3.client('s3')
    s3_bucket_name = os.getenv('AWS_BUCKET_NAME')

    try:
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': s3_bucket_name,
                'Key': key_name,
                'ContentType': f"image/{file_extension}"
            },
            ExpiresIn=IMG_TIMEOUT
        )
        return presigned_url
    except NoCredentialsError:
        print("Credentials not available")
        return None


def generate_video_presigned_url(image_name: str, email: str, content_id: int, db):
    valid_extensions = [
        ".MOV",
        ".MPEG-1",
        ".MPEG-2",
        ".mp4",  # Corrected from ".MPEG4" to ".mp4"
        ".MP4",
        ".MPG",
        ".AVI",
        ".WMV",
        ".MPEGPS",
        ".FLV",
        ".3GPP",
        ".WebM",
        ".DNxHR",
        ".ProRes",
        ".CineForm",
        ".HEVC"  # Assuming the file extension for HEVC is ".HEVC"
    ]
    file_extension = image_name.split('.')[-1].lower()

    if file_extension not in valid_extensions:
        print("")
        return None

    # append UUID to image name
    uuid_value = uuid.uuid4()
    key_name = f"videos/{uuid_value}/{image_name}"

    # save the entry in db with pending status
    crud.add_video(content_id, key_name, email, enums.UploadStatus.pending, db)

    # init AWS client
    init_aws_client()

    # create AWS stuff
    s3_client = boto3.client('s3')
    s3_bucket_name = os.getenv('AWS_BUCKET_NAME')

    try:
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': s3_bucket_name,
                'Key': key_name,
                'ContentType': f"video/{file_extension}"
            },
            ExpiresIn=IMG_TIMEOUT
        )
        return presigned_url
    except NoCredentialsError:
        print("Credentials not available")
        return None
