from settings import settings
import boto3
from botocore.config import Config


__all__ = ["get_presigned_post"]


def get_presigned_post(file_name):
    config = Config(s3={"use_accelerate_endpoint": True})
    s3 = boto3.client(
        service_name="s3",
        region_name="ap-northeast-2",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        config=config,
    )
    presigned_post = s3.generate_presigned_post(
        Bucket=settings.S3_BUCKET,
        Key=file_name,
        Fields={
            "acl": "public-read",
        },
        Conditions=[
            {"acl": "public-read"},
        ],
        ExpiresIn=100,
    )

    print(presigned_post)

    return presigned_post
